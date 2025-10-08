from ttoken import TOKEN


TIPOS_ACEITOS = {
    TOKEN.INT: [TOKEN.valorInt],
    TOKEN.FLOAT: [TOKEN.valorInt, TOKEN.valorFloat],
    TOKEN.CHAR: [TOKEN.CHAR, TOKEN.valorString],
}


class Semantico:
    def __init__(self):
        # escopos são dicts com nome das funções
        self.scopes = [{}]
        self.defined_functions = {}

    """ Empilha """

    def add_scope(self, name):
        self.scopes.append({name: self.defined_functions[name]})

    """ desempilha """

    def rem_scope(self):
        self.scopes.pop()

    """Verifica compatibilidade de tipos em operações ou atribuições."""

    def verifica_tipo(self, tipo_esperado, tipo_recebido):
        if tipo_esperado != tipo_recebido:
            raise Exception(
                f"Erro semântico: Tipo incompatível. Esperado {tipo_esperado}, mas recebido {tipo_recebido}."
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

    def get_type_token(self, ident, linha, coluna):
        try:
            for escopo in self.scopes:
                if ident in escopo:
                    return escopo[ident][0]
                else:
                    if ident in escopo[ident][1].keys():
                        return escopo[0][1][ident][1]

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
