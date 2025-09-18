from enum import IntEnum


class TOKEN(IntEnum):
    # TODO: verificar se irá utilizar algo para leitura e escrita
    erro = 1
    eof = 2
    ident = 3
    num = 4
    string = 5
    IF = 6
    ELSE = 7
    WHILE = 8
    BEGIN = 9
    END = 10
    PROGRAM = 11
    abrePar = 12
    fechaPar = 13
    virg = 14
    ptoVirg = 15
    pto = 16
    igual = 17
    diferente = 18
    menor = 19
    menorIgual = 20
    maior = 21
    maiorIgual = 22
    AND = 23
    OR = 24
    NOT = 25
    mais = 26
    menos = 27
    multiplica = 28
    divide = 29
    porcent = 36
    LEIA = 30
    ESCREVA = 31
    VAR = 32
    abreChave = 33
    fechaChave = 34
    atrib = 35
    resto = 36
    BREAK = 37
    CONTINUE = 38
    RETURN = 39
    INT = 40
    FLOAT = 41
    CHAR = 42

    @classmethod
    def msg(cls, token):
        nomes = {
            1: "erro",
            2: "<eof>",
            3: "ident",
            4: "numero",
            5: "string",
            6: "if",
            7: "else",
            8: "while",
            9: "inicio",
            10: "fim",
            11: "program",
            12: "(",
            13: ")",
            14: ",",
            15: ";",
            16: ".",
            17: "==",
            18: "!=",
            19: "<",
            20: "<=",
            21: ">",
            22: ">=",
            23: "and",
            24: "or",
            25: "not",
            26: "+",
            27: "-",
            28: "*",
            29: "/",
            30: "leia",
            31: "escreva",
            32: "var",
            33: "{",
            34: "}",
            35: "=",
            36: "%",
            37: "break",
            38: "continue",
            39: "return",
            40: "int",
            41: "float",
            42: "char",
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            "program": TOKEN.PROGRAM,
            "if": TOKEN.IF,
            "while": TOKEN.WHILE,
            "inicio": TOKEN.BEGIN,
            "fim": TOKEN.END,
            "else": TOKEN.ELSE,
            "leia": TOKEN.LEIA,
            "escreva": TOKEN.ESCREVA,
            "var": TOKEN.VAR,
            "and": TOKEN.AND,
            "or": TOKEN.OR,
            "not": TOKEN.NOT,
            "int": TOKEN.INT,
            "float": TOKEN.FLOAT,
            "char": TOKEN.CHAR,
            "break": TOKEN.BREAK,
            "continue": TOKEN.CONTINUE,
            "return": TOKEN.RETURN,
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
