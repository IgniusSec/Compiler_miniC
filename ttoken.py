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

    @classmethod
    def tabelaOperacoes(cls):
        table = {}

        # --- Helper para Operações Binárias (Bi-direcionais) ---
        # Registra (A, op, B) e automaticamente (B, op, A) se forem diferentes
        def binaria(tipo1, op, tipo2, resultado):
            # Registra a forma padrão: int + float
            chave1 = (tipo1, op, tipo2)
            table[chave1] = resultado

            # Se os tipos forem diferentes, registra o inverso: float + int
            if tipo1 != tipo2:
                chave2 = (tipo2, op, tipo1)
                table[chave2] = resultado

        # --- Helper para Operações Unárias ---
        # Registra apenas (op, A)
        def unaria(op, tipo1, resultado):
            table[(op, tipo1)] = resultado

        # Definições curtas para legibilidade (opcional, mas ajuda)
        INT_T = TOKEN.valorInt
        FLOAT_T = TOKEN.valorFloat

        # ==========================================
        # 1. ARITMÉTICA
        # ==========================================

        # Int com Int
        binaria(INT_T, TOKEN.mais, INT_T, INT_T)
        binaria(INT_T, TOKEN.menos, INT_T, INT_T)
        binaria(INT_T, TOKEN.multiplica, INT_T, INT_T)
        binaria(INT_T, TOKEN.divide, INT_T, INT_T)
        binaria(INT_T, TOKEN.resto, INT_T, INT_T)

        # Float com Float
        binaria(FLOAT_T, TOKEN.mais, FLOAT_T, FLOAT_T)
        binaria(FLOAT_T, TOKEN.menos, FLOAT_T, FLOAT_T)
        binaria(FLOAT_T, TOKEN.multiplica, FLOAT_T, FLOAT_T)
        binaria(FLOAT_T, TOKEN.divide, FLOAT_T, FLOAT_T)

        # Misto (Int e Float) -> Retorna Float
        # A mágica acontece aqui: a função 'binaria' vai criar
        # as chaves (Int, +, Float) E (Float, +, Int) automaticamente.
        binaria(INT_T, TOKEN.mais, FLOAT_T, FLOAT_T)
        binaria(INT_T, TOKEN.menos, FLOAT_T, FLOAT_T)
        binaria(INT_T, TOKEN.multiplica, FLOAT_T, FLOAT_T)
        binaria(INT_T, TOKEN.divide, FLOAT_T, FLOAT_T)

        # ==========================================
        # 2. RELACIONAIS (Retornam Int/Booleano)
        # ==========================================
        binaria(INT_T, TOKEN.opRel, INT_T, INT_T)
        binaria(FLOAT_T, TOKEN.opRel, FLOAT_T, INT_T)
        binaria(INT_T, TOKEN.opRel, FLOAT_T, INT_T)  # Gera ambos os casos

        # ==========================================
        # 3. LÓGICAS (Apenas Int)
        # ==========================================
        binaria(INT_T, TOKEN.AND, INT_T, INT_T)
        binaria(INT_T, TOKEN.OR, INT_T, INT_T)
        unaria(TOKEN.NOT, INT_T, INT_T)

        # ==========================================
        # 4. UNÁRIAS ARITMÉTICAS (+a, -a)
        # ==========================================
        unaria(TOKEN.mais, INT_T, INT_T)
        unaria(TOKEN.menos, INT_T, INT_T)
        unaria(TOKEN.mais, FLOAT_T, FLOAT_T)
        unaria(TOKEN.menos, FLOAT_T, FLOAT_T)

        return table
