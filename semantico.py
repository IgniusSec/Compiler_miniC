from ttoken import TOKEN, OPREL as OPREL
import copy

vars_type = [TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR]


def type_var(var):
    if var == TOKEN.INT:
        return TOKEN.valorInt
    elif var == TOKEN.FLOAT:
        return TOKEN.valorFloat
    elif var == TOKEN.CHAR:
        return TOKEN.valorChar
    else:
        return var


def returnTypeOfVars(vet):
    i = 0
    aux = []
    while i < len(vet):
        aux.append(type_var(vet[i]))
        i += 1

    return aux


class ErroFunction(Exception):
    def __init__(self, esperado, recebido, msg):
        mensagem = (
            f"{msg}\n"
            f"Tokens esperado: {TOKEN.msg(esperado)}\n"
            f"Token recebido: {TOKEN.msg(recebido)}"
        )
        super().__init__(mensagem)


class ErroFunctionParams(Exception):
    def __init__(self, esperado, recebido):
        mensagem = f"Número de parametros incorretos: Esperado {esperado} | Recebido {recebido}"
        super().__init__(mensagem)


class ErroTipo(Exception):
    def __init__(self, msg):
        mensagem = f"Erro de operação: {msg}"
        super().__init__(mensagem)


class ErroSemantico(Exception):
    def __init__(self, permitidos, recebido, msg):
        mensagem = ""
        if isinstance(permitidos, list):
            mensagem = (
                f"{msg}\n"
                f"Tokens permitidos: {', '.join(TOKEN.msg(t) for t in permitidos)}\n"
                f"Token recebido: {TOKEN.msg(recebido)}"
            )
        else:
            mensagem = (
                f"{msg}\n"
                f"Tokens esperado: {TOKEN.msg(permitidos)}\n"
                f"Token recebido: {TOKEN.msg(recebido)}"
            )
        super().__init__(mensagem)


class Semantico:
    def __init__(self, arq):
        # escopos são dicts com nome das funções
        self.scopes = [{}]
        self.defined_functions = {}
        self.tipos_atrib = []
        self.arq = open(arq, "wt")
        self.tabelaOperacoes = TOKEN.tabelaOperacoes()

        # funções predefinidas
        self.new_function("putchar", TOKEN.valorChar, {"x": (TOKEN.valorChar, 0)})
        self.new_function("getchar", TOKEN.valorChar, dict())

        self.new_function("putint", TOKEN.valorInt, {"x": (TOKEN.valorInt, 0)})
        self.new_function("getint", TOKEN.valorInt, dict())

        self.new_function("putfloat", TOKEN.valorFloat, {"x": (TOKEN.valorFloat, 0)})
        self.new_function("getfloat", TOKEN.valorFloat, dict())

        self.new_function("putstr", TOKEN.valorString, {"x": (TOKEN.valorInt, 0)})
        self.new_function("getstr", TOKEN.valorString, dict())

    def end_semantico(self):
        self.arq.close()

    """ Empilha """

    def add_scope(self, name):
        self.scopes.append({name: copy.deepcopy(self.defined_functions[name])})

    """ desempilha """

    def rem_scope(self):
        self.scopes.pop()

    def verifica_atribs(self, vetor_tipos: list):
        esperado = vetor_tipos.pop(0)
        esperado = type_var(esperado)
        if len(vetor_tipos) > 1:
            table = tuple(returnTypeOfVars(vetor_tipos))
        else:
            table = (TOKEN.mais, type_var(vetor_tipos[0]))
        keys = self.tabelaOperacoes.keys()
        if table in self.tabelaOperacoes.keys():
            result = self.tabelaOperacoes[table]
            if result != esperado:
                raise ErroTipo(
                    f"{TOKEN.msg(esperado)} {TOKEN.msg(vetor_tipos[1])} {TOKEN.msg(vetor_tipos[2])}"
                )
        else:
            if len(vetor_tipos) > 1:
                raise ErroTipo(
                    f"{TOKEN.msg(esperado)} {TOKEN.msg(vetor_tipos[1])} {TOKEN.msg(vetor_tipos[2])}"
                )
            else:
                raise ErroTipo(f"{TOKEN.msg(esperado)} {TOKEN.msg(vetor_tipos[0])}")

    """Verifica compatibilidade de tipos em operações ou atribuições."""

    def verifica_tipo(self, vetor_tipos: list, function):
        if len(vetor_tipos) > 2:
            if TOKEN.opRel in vetor_tipos:
                aux = len(vetor_tipos)
                div = []
                div.append([])
                control1 = 0
                for i in range(aux):
                    if vetor_tipos[i] == TOKEN.ptoVirg:
                        div.append([])
                        control1 += 1
                    else:
                        div[control1].append(vetor_tipos[i])

                for vet in div:
                    if TOKEN.opRel in vet:
                        table = tuple(returnTypeOfVars(vet))
                        if table not in self.tabelaOperacoes.keys():
                            raise ErroTipo(
                                f"{TOKEN.msg(vetor_tipos[0])} {TOKEN.msg(vetor_tipos[1])} {TOKEN.msg(vetor_tipos[2])}"
                            )
                    else:
                        self.verifica_atribs(vet)

            elif not function:
                self.verifica_atribs(vetor_tipos)
            else:
                funcao_atual = self.defined_functions[function]
                tipo_retorno = vetor_tipos.pop(0)

                # verifica quantia de parametros da função
                totParamFunc = len(funcao_atual[1])
                totParamsPassed = len(vetor_tipos)
                if totParamFunc != totParamsPassed:
                    raise ErroFunctionParams(totParamFunc, totParamsPassed)

                tipo_retorno = type_var(tipo_retorno)
                tipo_func = funcao_atual[0]
                tipo_func = type_var(tipo_func)

                # verifica se o tipo da var de recebimento do retorno da função é igual ao tipo da função
                if tipo_func != tipo_retorno:
                    raise ErroSemantico(
                        tipo_func,
                        tipo_retorno,
                        f"Erro no tipo de retorno da função {function}",
                    )

                args = funcao_atual[1]
                for tipo_input, (name_param, resto_param) in zip(
                    vetor_tipos, args.items()
                ):
                    tipo_input = type_var(tipo_input)
                    resto_param = type_var(resto_param[0])
                    if tipo_input != resto_param:
                        raise ErroSemantico(
                            resto_param,
                            tipo_input,
                            f"Erro em um dos parâmetros da função: {function}",
                        )
        else:
            if function:
                raise ErroFunctionParams(
                    len(self.defined_functions[function][1]), len(vetor_tipos) - 1
                )

    """ define o scopo atual, colocando-o no final da pilha 
        retorno é o tipo de retorno e vars englobam tanto os parametros
        quanto as variaveis locais
    """

    def new_function(self, name, retorno, vars: dict):
        if name in self.defined_functions.keys():
            raise Exception(f'Erro semântico: Redeclaração da função "{name}"')
        self.defined_functions[name] = (retorno, vars)

    def is_function(self, ident):
        if ident in self.defined_functions.keys():
            return True
        return False

    def declare(self, name, type, tam_vet):
        # topo da pilha
        scope = self.scopes[-1]

        # scope = {funct: (retorno, vars)}
        if name in scope[-1].keys():
            raise Exception(
                f'Erro semântico: Redeclaração de "{name}" no mesmo escopo.'
            )

    def get_type_function(self, ident):
        if self.is_function(ident):
            return self.defined_functions[ident][0]
        else:
            raise Exception(f"Função não declarada: {ident}")

    def get_type_token(self, ident, linha, coluna):
        escopo = self.scopes[-1]
        try:
            if self.is_function(ident):
                return self.defined_functions[ident][0]
            else:
                vars = next(iter(escopo.values()))
                vars = vars[1]
                if ident in vars.keys():
                    return vars[ident][0]

            raise Exception(
                f'Variável "{ident}" não declarada. Linha: {linha}, coluna: {coluna}'
            )
        except Exception as e:
            print(f"Erro inesperado: {e}")
            exit(1)

    def define_scope(self, name, tipo, is_vetor):
        # topo da pilha
        scope_now = self.scopes[-1]

        scope = next(iter(scope_now))
        vars = next(iter(scope_now.values()))
        vars = vars[1]

        if name in vars.keys():
            raise Exception(
                f'Erro semântico: Redeclaração de "{name}" no mesmo escopo.'
            )

        vars[name] = (tipo, is_vetor)
        scope_now[scope] = (scope_now[scope][0], vars)

    def generate_code(self, nivel, codigo):
        ident = " " * 4 * nivel
        linha = ident + codigo
        self.arq.write(linha)

    def generate_function(self, nivel, funcao):
        # tipo de retorno e tipo dos parametros foi ignorado mas pode ser adicionado caso necessário
        func = self.defined_functions[funcao]
        # retorno = func[0]
        args = func[1]

        texto = f"def {funcao}("

        keys = list(args.keys())
        lim = len(args.items())
        for i in range(lim):
            texto += f"{keys[i]}: {TOKEN.msg(args[keys[i]][0])}"
            if i < (lim - 1):
                texto += ", "
            else:
                texto += ")"

        texto += f" -> {TOKEN.msg(func[0])}:\n"

        self.generate_code(nivel, texto)
