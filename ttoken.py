from enum import IntEnum

OPREL = [">", "<", ">=", "<=", "==", "!="]


class TOKEN(IntEnum):
    erro = 1
    eof = 2
    ident = 3
    valorString = 4
    IF = 5
    ELSE = 6
    WHILE = 7
    abrePar = 8
    fechaPar = 9
    virg = 10
    ptoVirg = 11
    pto = 12
    opRel = 13  # substitui <, >, <=, >=, ==, !=
    AND = 14
    OR = 15
    NOT = 16
    mais = 17
    menos = 18
    multiplica = 19
    divide = 20
    resto = 21
    FOR = 22
    VAR = 23
    abreChave = 24
    fechaChave = 25
    atrib = 26
    BREAK = 27
    CONTINUE = 28
    RETURN = 29
    INT = 30
    FLOAT = 31
    CHAR = 32
    valorInt = 33
    valorChar = 34
    valorFloat = 35
    abreCol = 36
    fechaCol = 37

    @classmethod
    def msg(cls, token):
        if token in OPREL:
            return "opRel"

        nomes = {
            1: "erro",
            2: "<eof>",
            3: "ident",
            4: "valorString",
            5: "if",
            6: "else",
            7: "while",
            8: "(",
            9: ")",
            10: ",",
            11: ";",
            12: ".",
            13: "opRel",  # operador de relação genérico
            14: "&&",
            15: "||",
            16: "!",
            17: "+",
            18: "-",
            19: "*",
            20: "/",
            21: "%",
            22: "for",
            23: "var",
            24: "{",
            25: "}",
            26: "=",
            27: "break",
            28: "continue",
            29: "return",
            30: "int",
            31: "float",
            32: "char",
            33: "valorInt",
            34: "valorChar",
            35: "valorFloat",
            36: "[",
            37: "]",
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            "if": TOKEN.IF,
            "while": TOKEN.WHILE,
            "else": TOKEN.ELSE,
            "var": TOKEN.VAR,
            "not": TOKEN.NOT,
            "int": TOKEN.INT,
            "float": TOKEN.FLOAT,
            "char": TOKEN.CHAR,
            "break": TOKEN.BREAK,
            "continue": TOKEN.CONTINUE,
            "return": TOKEN.RETURN,
            "for": TOKEN.FOR,
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
