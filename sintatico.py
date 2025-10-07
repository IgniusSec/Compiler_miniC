from lexical import Lexical, PATH_FILE
from ttoken import TOKEN
import sys

import ttoken

PERM_TYPES = [TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR, TOKEN.VOID]


class Sintatico:

    def __init__(self, lexico: Lexical):
        self.lexico = lexico
        self.lexico.token_atual = self.lexico.get_token()

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
        self.type()
        self.consume(TOKEN.ident)
        self.consume(TOKEN.abrePar)
        self.arg_list()
        self.consume(TOKEN.fechaPar)
        self.compound_stmt()

    """
        ArgList ->  Arg RestoArgList | LAMBDA
    """

    def arg_list(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        # TODO: verificar se a comparação está correta
        if token in PERM_TYPES:
            self.arg()
            self.resto_arg_list()
        else:
            return

    """
        RestoArgList -> , Arg RestoArgList | LAMBDA
    """

    def resto_arg_list(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.arg()
            self.resto_arg_list()
        else:
            return

    """
        Arg -> Type IdentArg
    """

    def arg(self):
        self.type()
        self.ident_arg()

    """
        IdentArg -> ident OpcIdentArg
    """

    def ident_arg(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ident:
            self.consume(TOKEN.ident)
            self.opc_ident_arg()
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        OpcIdentArg ->  [ ] | LAMBDA
    """

    def opc_ident_arg(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)
            self.consume(TOKEN.fechaCol)
        else:
            return

    """
        CompoundStmt ->  { StmtList }
    """

    def compound_stmt(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreChave:
            self.consume(TOKEN.abreChave)
            self.stmt_list()
            self.consume(TOKEN.fechaChave)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        StmtList ->  Stmt StmtList | LAMBDA
    """

    def stmt_list(self):
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
            self.stmt()
            self.stmt_list()
        else:
            return

    """
        Stmt -> ForStmt | WhileStmt | IfStmt
        | CompoundStmt | break ;
        | continue ; | return Expr ; 
        | Expr ; | Declaration | ;
    """

    def stmt(self):
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
            self.for_stmt()
        elif token == TOKEN.WHILE:
            self.while_stmt()
        elif token == TOKEN.IF:
            self.if_stmt()
        elif token == TOKEN.abreChave:
            self.compound_stmt()
        elif token == TOKEN.BREAK:
            self.consume(TOKEN.BREAK)
            self.consume(TOKEN.ptoVirg)
        elif token == TOKEN.CONTINUE:
            self.consume(TOKEN.CONTINUE)
            self.consume(TOKEN.ptoVirg)
        elif token == TOKEN.RETURN:
            self.consume(TOKEN.RETURN)
            self.expr()
            self.consume(TOKEN.ptoVirg)
        elif token in pred:
            self.expr()
            self.consume(TOKEN.ptoVirg)
        elif token in PERM_TYPES:
            self.declaration()
        elif token == TOKEN.ptoVirg:
            self.consume(TOKEN.ptoVirg)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        ForStmt -> for ( Expr ; OptExpr ; OptExpr ) Stmt
    """

    def for_stmt(self):
        self.consume(TOKEN.FOR)
        self.consume(TOKEN.abrePar)
        self.expr()
        self.consume(TOKEN.ptoVirg)
        self.opt_expr()
        self.consume(TOKEN.ptoVirg)
        self.opt_expr()
        self.consume(TOKEN.fechaPar)
        self.stmt()

    """
        OptExpr -> Expr | LAMBDA
    """

    def opt_expr(self):
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
            self.expr()
        else:
            return

    """
        WhileStmt -> while ( Expr ) Stmt
    """

    def while_stmt(self):
        self.consume(TOKEN.WHILE)
        self.consume(TOKEN.abrePar)
        self.expr()
        self.consume(TOKEN.fechaPar)
        self.stmt()

    """
        IfStmt -> if ( Expr ) Stmt ElsePart
    """

    def if_stmt(self):
        self.consume(TOKEN.IF)
        self.consume(TOKEN.abrePar)
        self.expr()
        self.consume(TOKEN.fechaPar)
        self.stmt()
        self.else_part()

    """
        ElsePart -> else Stmt | LAMBDA
    """

    def else_part(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ELSE:
            self.consume(TOKEN.ELSE)
            self.stmt()
        else:
            return

    """
        Declaration -> Type IdentList ;
    """

    def declaration(self):
        self.type()
        self.ident_list()
        self.consume(TOKEN.ptoVirg)

    """
        Type -> int | float | char
    """

    def type(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.INT:
            self.consume(TOKEN.INT)
        elif token == TOKEN.FLOAT:
            self.consume(TOKEN.FLOAT)
        elif token == TOKEN.CHAR:
            self.consume(TOKEN.CHAR)
        elif token == TOKEN.VOID:
            self.consume(TOKEN.VOID)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        IdentList -> IdentDeclar RestoIdentList
    """

    def ident_list(self):
        self.ident_declar()
        self.resto_ident_list()

    """
        RestoIdentList -> , IdentDeclar RestoIdentList | LAMBDA
    """

    def resto_ident_list(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.ident_declar()
            self.resto_ident_list()
        else:
            return

    """
        IdentDeclar   ->  ident OpcIdentDeclar
    """

    def ident_declar(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.ident:
            self.consume(TOKEN.ident)
            self.opc_ident_declar()
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        OpcIdentDeclar  ->  [ valorInt ] | LAMBDA
    """

    def opc_ident_declar(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)
            self.consume(TOKEN.valorInt)
            self.consume(TOKEN.fechaCol)
        # retirando possibilidade de atribuição de valor na declaração da variável
        # elif token == TOKEN.atrib:
        #     self.consume(TOKEN.atrib)
        #     self.expr()
        else:
            return

    """
        Expr -> Log RestoExpr
    """

    def expr(self):
        self.log()
        self.resto_expr()

    """
        RestoExpr ->  = Expr RestoExpr | LAMBDA
    """

    def resto_expr(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.atrib:
            self.consume(TOKEN.atrib)
            self.expr()
            self.resto_expr()
        else:
            return

    """
        Log -> Nao RestoLog
    """

    def log(self):
        self.nao()
        self.resto_log()

    """
        RestoLog -> AND Nao RestoLog | OR Nao RestoLog | LAMBDA
    """

    def resto_log(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.AND:
            self.consume(TOKEN.AND)
            self.nao()
            self.resto_log()
        elif token == TOKEN.OR:
            self.consume(TOKEN.OR)
            self.nao()
            self.resto_log()
        else:
            return

    """
        Nao -> NOT Nao | Rel
    """

    def nao(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.NOT:
            self.consume(TOKEN.NOT)
            self.nao()
        else:
            self.rel()

    """
        Rel ->  Soma RestoRel
    """

    def rel(self):
        self.soma()
        self.resto_rel()

    """
        RestoRel ->  opRel Soma | LAMBDA
    """

    def resto_rel(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.opRel:
            self.consume(TOKEN.opRel)
            self.soma()
        else:
            return

    """
        Soma -> Mult RestoSoma
    """

    def soma(self):
        self.mult()
        self.resto_soma()

    """
        RestoSoma ->  + Mult RestoSoma | - Mult RestoSoma | LAMBDA
    """

    def resto_soma(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.mais:
            self.consume(TOKEN.mais)
            self.mult()
            self.resto_soma()
        elif token == TOKEN.menos:
            self.consume(TOKEN.menos)
            self.mult()
            self.resto_soma()
        else:
            return

    """
        Mult ->  Uno RestoMult
    """

    def mult(self):
        self.uno()
        self.resto_mult()

    """
        RestoMult ->  * Uno RestoMult | / Uno RestoMult
        | % Uno RestoMult | LAMBDA
    """

    def resto_mult(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.multiplica:
            self.consume(TOKEN.multiplica)
            self.uno()
            self.resto_mult()
        elif token == TOKEN.divide:
            self.consume(TOKEN.divide)
            self.uno()
            self.resto_mult()
        elif token == TOKEN.resto:
            self.consume(TOKEN.resto)
            self.uno()
            self.resto_mult()
        else:
            return

    """
        Uno -> + Uno | - Uno | Folha
    """

    def uno(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.mais:
            self.consume(TOKEN.mais)
            self.uno()
        elif token == TOKEN.menos:
            self.consume(TOKEN.menos)
            self.uno()
        else:
            self.folha()

    """
        Folha -> ( Expr ) | Identifier
        | valorInt | valorFloat | valorChar | valorString
    """

    def folha(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abrePar:
            self.consume(TOKEN.abrePar)
            self.expr()
            self.consume(TOKEN.fechaPar)
        elif token == TOKEN.ident:
            self.identifier()
        elif token == TOKEN.valorInt:
            self.consume(TOKEN.valorInt)
        elif token == TOKEN.valorFloat:
            self.consume(TOKEN.valorFloat)
        elif token == TOKEN.valorChar:
            self.consume(TOKEN.valorChar)
        elif token == TOKEN.valorString:
            self.consume(TOKEN.valorString)
        else:
            self.error_message(token, lexema, linha, coluna)

    """
        Identifier ->  ident OpcIdentifier
    """

    def identifier(self):
        self.consume(TOKEN.ident)
        self.opc_identifier()

    """
        OpcIdentifier ->  [ Expr ] | ( Params ) | LAMBDA
    """

    def opc_identifier(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.abreCol:
            self.consume(TOKEN.abreCol)
            self.expr()
            self.consume(TOKEN.fechaCol)
        elif token == TOKEN.abrePar:
            self.consume(TOKEN.abrePar)
            self.params()
            self.consume(TOKEN.fechaPar)
        else:
            return

    """
        Params ->  Expr RestoParams | LAMBDA
    """

    def params(self):
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
            self.expr()
            self.resto_params()
        else:
            return

    """
        RestoParams  ->  , Expr RestoParams | LAMBDA
    """

    def resto_params(self):
        (token, lexema, linha, coluna) = self.lexico.token_atual
        if token == TOKEN.virg:
            self.consume(TOKEN.virg)
            self.expr()
            self.resto_params()
        else:
            return


if __name__ == "__main__":
    path = "testeErro.c"
    lex = Lexical(path)
    sintatico = Sintatico(lex)

    sintatico.program()
