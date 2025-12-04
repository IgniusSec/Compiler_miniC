from lexical import Lexical, PATH_FILE
from ttoken import TOKEN
from semantico import Semantico, ErroFunctionParams

PERM_TYPES = [TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR]


class ErrorSintatico(Exception):
    def __init__(self, msg, linha, coluna):
        mensagem = f"{msg}\n"
        mensagem += f"\nLinha {linha} x Coluna {coluna}"
        super().__init__(mensagem)


class Sintatico:

    def __init__(self, lexico: Lexical, arq_semantico: str):
        self.lexico = lexico
        self.lexico.token_atual = self.lexico.get_token()
        self.semantico = Semantico(arq_semantico)

        self.semantico.generate_code(0, '\nif __name__ == "__main__":\n', 0)
        self.semantico.generate_code(1, "main()\n\n\n", 0)

    def error_message(self, token, lexema, linha, coluna):
        msg = TOKEN.msg(token)
        print(f"Comando mal utilizado: {msg}: {lexema} || Lin{linha} Col{coluna}")
        raise Exception("Command unknow")

    def test_lexico(self):
        self.lexico.token_atual = self.lexico.get_token()
        (token, lexema, linha, coluna) = self.lexico.token_atual
        while token != TOKEN.eof:
            self.lexico.print_token(self.lexico.token_atual)
            self.lexico.token_atual = self.lexico.get_token()
            (token, lexema, linha, coluna) = self.lexico.token_atual

    def consume(self, token_now):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token_now == token:
            if token != TOKEN.eof:
                self.lexico.token_atual = self.lexico.get_token()
        else:
            msg_token_lido = TOKEN.msg(token)
            msg_token_now = TOKEN.msg(token_now)
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msg_token_lido
                print(
                    f"Esperado: {msg_token_now} || Recebido: {msg}\nLin {linha} Col {coluna}"
                )
                raise Exception(f"Token doesn't match: {msg}")

    def verifica_tipos(self, lexema, linha, coluna):
        # verifica se os tipos atribuidos são válidos
        # verifica se há mais de um elemento na lista
        if len(self.semantico.tipos_atrib) > 1:
            if self.semantico.is_function(lexema):
                self.semantico.verifica_tipo(
                    self.semantico.tipos_atrib, lexema, linha, coluna
                )
            else:
                self.semantico.verifica_tipo(
                    self.semantico.tipos_atrib, None, linha, coluna
                )
        elif self.semantico.is_function(lexema):
            raise ErroFunctionParams(
                len(self.semantico.defined_functions[lexema][1]), 0, linha, coluna
            )

    """
        Program  ->  LAMBDA | Function Program
    """

    def program(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual

        if token in PERM_TYPES:
            self.function()
            self.program()

        else:
            return

    """
        Function  ->  Type ident ( ArgList ) CompoundStmt
    """

    def function(self):
        retorno = self.type()
        name = self.lexico.token_atual
        # filtra o nome da função baseado no token atual
        name = name[1]
        self.consume(TOKEN.ident)
        self.consume(TOKEN.abrePar)
        args = self.arg_list()
        self.consume(TOKEN.fechaPar)

        # cria a função
        self.semantico.new_function(name, retorno, args)
        self.semantico.generate_function(0, name)

        # abre o escopo daquela função
        self.semantico.add_scope(name)
        self.compound_stmt(1)
        self.semantico.rem_scope()
        self.semantico.generate_code(0, "\n\n", 0)

    """
        ArgList ->  Arg RestoArgList | LAMBDA
    """

    def arg_list(self):
        args = {}
        (token, lexema, linha, coluna) = self.lexico.token_atual
        # TODO: verificar se a comparação está correta
        if token in PERM_TYPES:
            (name, tipo, is_vetor) = self.arg()
            args[name] = (tipo, is_vetor)
            self.resto_arg_list(args)

        return args

    """
        RestoArgList -> , Arg RestoArgList | LAMBDA
    """

    def resto_arg_list(self, args):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            (name, tipo, is_vetor) = self.arg()
            if name in args.keys():
                raise ErrorSintatico(f"Erro, {name} já foi declarado!", linha, coluna)
            args[name] = (tipo, is_vetor)
            self.resto_arg_list(args)
        else:
            return

    """
        Arg -> Type IdentArg
    """

    def arg(self):
        tipo = self.type()
        (name, is_vetor) = self.ident_arg()

        return (name, tipo, is_vetor)

    """
        IdentArg -> ident OpcIdentArg
    """

    def ident_arg(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ident:
            name = lexema
            self.consume(TOKEN.ident)
            is_vetor = self.opc_ident_arg()
        else:
            self.error_message(token, lexema, linha, coluna)

        return (name, is_vetor)

    """
        OpcIdentArg ->  [ ] | LAMBDA
    """

    def opc_ident_arg(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)
            self.consume(TOKEN.fechaCol)

            # Retorna -1 para definir que o vetor não teve tamanho especificado mas é um vetor
            return -1
        else:
            return 0

    """
        CompoundStmt ->  { StmtList }
    """

    def compound_stmt(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreChave:
            self.consume(TOKEN.abreChave)

            self.stmt_list(ident)
            self.consume(TOKEN.fechaChave)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        StmtList ->  Stmt StmtList | LAMBDA
    """

    def stmt_list(self, ident):
        pred = [
            TOKEN.BREAK,
            TOKEN.CONTINUE,
            TOKEN.RETURN,
            TOKEN.ptoVirg,
            TOKEN.FOR,
            TOKEN.IF,
            TOKEN.WHILE,
            TOKEN.abreChave,
            TOKEN.NOT,
            TOKEN.mais,
            TOKEN.menos,
            TOKEN.abrePar,
            TOKEN.valorInt,
            TOKEN.valorFloat,
            TOKEN.valorChar,
            TOKEN.valorString,
            TOKEN.ident,
        ]
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token in pred or token in PERM_TYPES:
            self.stmt(ident)
            self.stmt_list(ident)
        else:
            return

    """
        Stmt -> ForStmt | WhileStmt | IfStmt
        | CompoundStmt | break ;
        | continue ; | return Expr ; 
        | Expr ; | Declaration | ;
    """

    def stmt(self, ident):
        # usado para verificar os tipos na atribuição
        self.semantico.tipos_atrib = []
        pred = [
            TOKEN.NOT,
            TOKEN.mais,
            TOKEN.menos,
            TOKEN.abrePar,
            TOKEN.valorInt,
            TOKEN.valorFloat,
            TOKEN.valorChar,
            TOKEN.valorString,
            TOKEN.ident,
        ]
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.FOR:
            self.for_stmt(ident, linha, coluna)
        elif token == TOKEN.WHILE:
            self.while_stmt(ident, linha, coluna)
        elif token == TOKEN.IF:
            self.if_stmt(ident, linha, coluna)
        elif token == TOKEN.abreChave:
            self.semantico.generate_code(0, "\n", 0)
            self.compound_stmt(ident)
        elif token == TOKEN.BREAK:
            self.consume(TOKEN.BREAK)
            self.consume(TOKEN.ptoVirg)
            self.semantico.generate_code(ident, "\n", 0)
        elif token == TOKEN.CONTINUE:
            self.consume(TOKEN.CONTINUE)
            self.consume(TOKEN.ptoVirg)
            self.semantico.generate_code(ident, "\n", 0)
        elif token == TOKEN.RETURN:
            self.consume(TOKEN.RETURN)
            self.semantico.generate_code(ident, "return", 1)
            self.expr(0)
            self.verifica_tipos(lexema, linha, coluna)
            self.consume(TOKEN.ptoVirg)
            self.semantico.generate_code(ident, "\n", 0)
        elif token in pred:  # atribuição
            self.expr(ident)
            self.verifica_tipos(lexema, linha, coluna)
            self.consume(TOKEN.ptoVirg)
            self.semantico.generate_code(ident, "\n", 0)
        elif token in PERM_TYPES:
            self.declaration(ident)
        elif token == TOKEN.ptoVirg:
            self.consume(TOKEN.ptoVirg)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        ForStmt -> for ( Expr ; OptExpr ; OptExpr ) Stmt
    """

    def for_stmt(self, ident, linha, coluna):
        self.consume(TOKEN.FOR)
        self.semantico.generate_code(ident, "for", 1)
        self.consume(TOKEN.abrePar)
        self.expr(0)
        self.consume(TOKEN.ptoVirg)
        self.semantico.tipos_atrib.append(TOKEN.ptoVirg)
        self.opt_expr(0)
        self.consume(TOKEN.ptoVirg)
        self.semantico.tipos_atrib.append(TOKEN.ptoVirg)
        self.opt_expr(0)
        self.consume(TOKEN.fechaPar)
        self.semantico.generate_code(0, ":", 0)
        self.verifica_tipos(None, linha, coluna)
        self.stmt(ident + 1)

    """
        OptExpr -> Expr | LAMBDA
    """

    def opt_expr(self, ident):
        pred = [
            TOKEN.NOT,
            TOKEN.mais,
            TOKEN.menos,
            TOKEN.abrePar,
            TOKEN.valorInt,
            TOKEN.valorFloat,
            TOKEN.valorChar,
            TOKEN.valorString,
            TOKEN.ident,
        ]

        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token in pred:
            self.expr(ident)
        else:
            return

    """
        WhileStmt -> while ( Expr ) Stmt
    """

    def while_stmt(self, ident, linha, coluna):
        self.consume(TOKEN.WHILE)
        self.semantico.generate_code(ident, "while", 1)
        self.consume(TOKEN.abrePar)
        self.expr(0)
        self.consume(TOKEN.fechaPar)
        self.semantico.generate_code(0, ":", 0)
        self.verifica_tipos(None, linha, coluna)
        self.stmt(ident + 1)

    """
        IfStmt -> if ( Expr ) Stmt ElsePart
    """

    def if_stmt(self, ident, linha, coluna):
        self.consume(TOKEN.IF)
        self.semantico.generate_code(ident, "if", 1)
        self.consume(TOKEN.abrePar)
        self.expr(0)
        self.consume(TOKEN.fechaPar)
        self.semantico.generate_code(0, ":", 0)
        self.verifica_tipos(None, linha, coluna)
        self.stmt(ident + 1)
        self.else_part(ident)

    """
        ElsePart -> else Stmt | LAMBDA
    """

    def else_part(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ELSE:
            self.consume(TOKEN.ELSE)
            self.semantico.generate_code(ident, "else", 0)
            self.semantico.generate_code(0, ":", 0)
            self.stmt(ident + 1)
        else:
            return

    """
        Declaration -> Type IdentList ;
    """

    def declaration(self, ident):
        tipo = self.type()
        self.ident_list(tipo)
        self.consume(TOKEN.ptoVirg)

    """
        Type -> int | float | char
    """

    def type(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.INT:
            self.consume(TOKEN.INT)
            return TOKEN.INT
        elif token == TOKEN.FLOAT:
            self.consume(TOKEN.FLOAT)
            return TOKEN.FLOAT
        elif token == TOKEN.CHAR:
            self.consume(TOKEN.CHAR)
            return TOKEN.CHAR
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        IdentList -> IdentDeclar RestoIdentList
    """

    def ident_list(self, tipo):
        self.ident_declar(tipo)
        self.resto_ident_list(tipo)

    """
        RestoIdentList -> , IdentDeclar RestoIdentList | LAMBDA
    """

    def resto_ident_list(self, tipo):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.ident_declar(tipo)
            self.resto_ident_list(tipo)
        else:
            return

    """
        IdentDeclar   ->  ident OpcIdentDeclar
    """

    def ident_declar(self, tipo):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ident:
            self.consume(TOKEN.ident)
            self.opc_ident_declar(tipo, lexema)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        OpcIdentDeclar  ->  [ valorInt ] | LAMBDA
    """

    def opc_ident_declar(self, tipo, name):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)

            is_vetor = self.lexico.token_atual

            self.consume(TOKEN.valorInt)
            self.consume(TOKEN.fechaCol)

            self.semantico.define_scope(name, tipo, is_vetor)
        # retirando possibilidade de atribuição de valor na declaração da variável
        # elif token == TOKEN.atrib:
        #     self.consume(TOKEN.atrib)
        #     self.expr()
        else:
            self.semantico.define_scope(name, tipo, 0)
            return

    """
        Expr -> Log RestoExpr
    """

    def expr(self, ident):
        self.log(ident)
        self.resto_expr(0)

    """
        RestoExpr ->  = Expr RestoExpr | LAMBDA
    """

    def resto_expr(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.atrib:
            self.consume(TOKEN.atrib)
            self.semantico.generate_code(0, "=", 1)
            self.expr(ident)
            self.resto_expr(ident)
        else:
            return

    """
        Log -> Nao RestoLog
    """

    def log(self, ident):
        self.nao(ident)
        self.resto_log(ident)

    """
        RestoLog -> AND Nao RestoLog | OR Nao RestoLog | LAMBDA
    """

    def resto_log(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.AND:
            self.consume(TOKEN.AND)
            self.semantico.generate_code(0, "and", 1)
            self.nao(ident)
            self.resto_log(ident)
        elif token == TOKEN.OR:
            self.consume(TOKEN.OR)
            self.semantico.generate_code(0, "or", 1)
            self.nao(ident)
            self.resto_log(ident)
        else:
            return

    """
        Nao -> NOT Nao | Rel
    """

    def nao(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.NOT:
            self.consume(TOKEN.NOT)
            self.semantico.generate_code(0, "not", 1)
            self.nao(ident)
        else:
            self.rel(ident)

    """
        Rel ->  Soma RestoRel
    """

    def rel(self, ident):
        self.soma(ident)
        self.resto_rel(ident)

    """
        RestoRel ->  opRel Soma | LAMBDA
    """

    def resto_rel(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.opRel:
            self.semantico.tipos_atrib.append(token)
            self.semantico.generate_code(0, lexema, 1)
            self.consume(TOKEN.opRel)
            self.soma(ident)
        else:
            return

    """
        Soma -> Mult RestoSoma
    """

    def soma(self, ident):
        self.mult(ident)
        self.resto_soma(ident)

    """
        RestoSoma ->  + Mult RestoSoma | - Mult RestoSoma | LAMBDA
    """

    def resto_soma(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.mais:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.mais)
            self.semantico.generate_code(0, lexema, 1)
            self.mult(ident)
            self.resto_soma(ident)
        elif token == TOKEN.menos:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.menos)
            self.semantico.generate_code(0, lexema, 1)
            self.mult(ident)
            self.resto_soma(ident)
        else:
            return

    """
        Mult ->  Uno RestoMult
    """

    def mult(self, ident):
        self.uno(ident)
        self.resto_mult(ident)

    """
        RestoMult ->  * Uno RestoMult | / Uno RestoMult
        | % Uno RestoMult | LAMBDA
    """

    def resto_mult(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.multiplica:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.multiplica)
            self.semantico.generate_code(0, lexema, 1)
            self.uno(ident)
            self.resto_mult(ident)
        elif token == TOKEN.divide:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.divide)
            self.semantico.generate_code(0, lexema, 1)
            self.uno(ident)
            self.resto_mult(ident)
        elif token == TOKEN.resto:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.resto)
            self.semantico.generate_code(0, lexema, 1)
            self.uno(ident)
            self.resto_mult(ident)
        else:
            return

    """
        Uno -> + Uno | - Uno | Folha
    """

    def uno(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.mais:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.mais)
            self.semantico.generate_code(0, lexema, 1)
            self.uno(ident)
        elif token == TOKEN.menos:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.menos)
            self.semantico.generate_code(0, lexema, 1)
            self.uno(ident)
        else:
            self.folha(ident)

    """
        Folha -> ( Expr ) | Identifier
        | valorInt | valorFloat | valorChar | valorString
    """

    def folha(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abrePar:
            self.consume(TOKEN.abrePar)
            self.semantico.generate_code(0, lexema, 1)
            self.expr(ident)
            self.consume(TOKEN.fechaPar)
            self.semantico.generate_code(0, ")", 0)
        elif token == TOKEN.ident:
            self.semantico.tipos_atrib.append(
                self.semantico.get_type_token(
                    lexema, self.lexico.linha, self.lexico.coluna
                )
            )

            if self.semantico.is_function(lexema):
                self.semantico.generate_code(ident, lexema, 0)
            else:
                self.semantico.generate_code(ident, lexema, 1)
            self.identifier(ident)
        elif token == TOKEN.valorInt:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.valorInt)
            self.semantico.generate_code(0, lexema, 1)
        elif token == TOKEN.valorFloat:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.valorFloat)
            self.semantico.generate_code(0, lexema, 1)
        elif token == TOKEN.valorChar:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.valorChar)
            self.semantico.generate_code(0, lexema, 1)
        elif token == TOKEN.valorString:
            self.semantico.tipos_atrib.append(token)
            self.consume(TOKEN.valorString)
            self.semantico.generate_code(0, lexema, 1)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        Identifier ->  ident OpcIdentifier
    """

    def identifier(self, ident):
        self.consume(TOKEN.ident)
        self.opc_identifier(ident)

    """
        OpcIdentifier ->  [ Expr ] | ( Params ) | LAMBDA
    """

    def opc_identifier(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)
            self.semantico.generate_code(0, lexema, 1)
            self.expr(0)
            self.consume(TOKEN.fechaCol)
            self.semantico.generate_code(0, "]", 0)
        elif token == TOKEN.abrePar:
            self.consume(TOKEN.abrePar)
            self.semantico.generate_code(0, lexema, 1)
            self.params(0)
            self.consume(TOKEN.fechaPar)
            self.semantico.generate_code(0, ")", 1)
        else:
            return

    """
        Params ->  Expr RestoParams | LAMBDA
    """

    def params(self, ident):
        pred = [
            TOKEN.NOT,
            TOKEN.mais,
            TOKEN.menos,
            TOKEN.abrePar,
            TOKEN.valorInt,
            TOKEN.valorFloat,
            TOKEN.valorChar,
            TOKEN.valorString,
            TOKEN.ident,
        ]

        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token in pred:
            self.expr(ident)
            self.resto_params(ident)
        else:
            return

    """
        RestoParams  ->  , Expr RestoParams | LAMBDA
    """

    def resto_params(self, ident):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.semantico.generate_code(ident, lexema, 1)
            self.expr(ident)
            self.resto_params(ident)
        else:
            return


if __name__ == "__main__":
    path = "example2.c"
    arq_sem = "testeSemantico.py"
    lex = Lexical(path)
    sintatico = Sintatico(lex, arq_sem)

    sintatico.program()
