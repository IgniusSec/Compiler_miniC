from ttoken import TOKEN, OPREL as OPREL


TIPOS_ACEITOS = {
    TOKEN.INT: [TOKEN.valorInt, TOKEN.INT],
    TOKEN.FLOAT: [TOKEN.valorInt, TOKEN.valorFloat, TOKEN.INT, TOKEN.FLOAT],
    TOKEN.CHAR: [TOKEN.CHAR, TOKEN.valorString],
}

TIPOS_NUMERICOS = [TOKEN.valorFloat, TOKEN.valorInt, TOKEN.INT, TOKEN.FLOAT]


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

    def end_semantico(self):
        self.arq.close()

    """ Empilha """

    def add_scope(self, name):
        self.scopes.append({name: self.defined_functions[name]})

    """ desempilha """

    def rem_scope(self):
        self.scopes.pop()

    """Verifica compatibilidade de tipos em operações ou atribuições."""

    def verifica_tipo(self, vetor_tipos: list, function):
        if any(op in vetor_tipos for op in OPREL):
            esperado = vetor_tipos.pop(0)
            permitidos = TIPOS_ACEITOS[esperado]
            for i in range(len(vetor_tipos)):
                if vetor_tipos[i] not in OPREL and vetor_tipos[i] not in permitidos:
                    raise ErroSemantico(permitidos, vetor_tipos[i], "Erro de relação")
        elif not function:
            esperado = vetor_tipos.pop(0)
            permitidos = TIPOS_ACEITOS[esperado]
            for rec in vetor_tipos:
                if rec not in permitidos:
                    raise ErroSemantico(permitidos, rec, "Erro na atribuição")
        else:
            funcao_atual = self.defined_functions[function]
            tipo_retorno = vetor_tipos.pop(0)
            tipo_func = funcao_atual[0]

            # verifica se o tipo da var de recebimento do retorno da função é igual ao tipo da função
            if tipo_func != tipo_retorno:
                raise ErroSemantico(
                    TIPOS_ACEITOS[tipo_retorno],
                    tipo_func,
                    f"Erro no tipo de retorno da função {function}",
                )

            args = funcao_atual[1]
            for tipo_input, (name_param, resto_param) in zip(vetor_tipos, args.items()):
                if tipo_input != resto_param[0]:
                    raise ErroSemantico(
                        resto_param[0],
                        tipo_input,
                        f"Erro em um dos parâmetros da função: {function}",
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
        texto = f"def {funcao}({','.join(args.keys())}):\n"

        self.generate_code(nivel, texto)
