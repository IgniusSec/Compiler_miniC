from ttoken import TOKEN
import sys

EXCLUDED_CHARS = [
    "(",
    ")",
    ",",
    ".",
    ";",
    "<",
    ">",
    "*",
    "+",
    "/",
    "-",
    "%",
    "=",
    "{",
    "}",
]
BROKEN_CHARS = ["\n", " "]
PATH_FILE = "exemplo.c"


class Lexical:
    def __init__(self, arq_path):
        self.arq = arq_path
        try:
            file = open(arq_path, "r")
            content = file.read()
            self.content = list(content)
            file.close()
        except FileNotFoundError:
            print("File not found!")
            return

        self.content.append("\0")

        self.arq_size = len(self.content)
        self.linha = 1
        self.coluna = 1

        self.index = 0
        self.comments = 0
        self.token_atual = None

    def end_of_file(self):
        return self.index >= (self.arq_size - self.comments)

    # pega um char
    def get_char(self):
        char = self.content[self.index]
        self.index += 1
        if char == "\n":
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return char

    def print_token(self, token_atual):
        (token, lexema, linha, coluna) = token_atual
        msg = TOKEN.msg(token)
        print(f"(message: {msg} || lex: {lexema} || lin {linha}, col {coluna})")

    # devolve char
    def unget_char(self, simbol):
        if simbol not in BROKEN_CHARS:
            if self.index > 0:
                self.index -= 1
            if self.coluna > 0:
                self.coluna -= 1

    # remove comentarios
    def trash_comments(self, index):
        aux = index
        while self.content[aux] != "\n":
            self.content.pop(aux)
            self.comments += 1
        # tira os \n pos comentário
        while self.content[aux] == "\n":
            self.content.pop(aux)
            self.linha += 1
            self.comments += 1

    """
        Retorna uma quadrupla com (tipo_token, token, linha do token, coluna do token)
    """

    def get_token(self):

        estado = 1
        lexema = ""
        char = self.get_char()

        if char in BROKEN_CHARS:
            while char in BROKEN_CHARS:
                self.unget_char(char)
                char = self.get_char()

        lin = self.linha
        col = self.coluna

        while True:
            if (char not in BROKEN_CHARS and char not in EXCLUDED_CHARS) or (
                estado == 4
            ):
                lexema += char
            if estado == 1:
                # letra/simbolo
                if char.isalpha() or char == "_":
                    estado = 2
                # numeros
                elif char.isdigit():
                    estado = 3
                # inicio de string
                elif char == '"':
                    estado = 4
                elif char == "(":
                    return (TOKEN.abrePar, "(", lin, col)
                elif char == ")":
                    return (TOKEN.fechaPar, ")", lin, col)
                elif char == "{":
                    return (TOKEN.abreChave, "{", lin, col)
                elif char == "}":
                    return (TOKEN.fechaChave, "}", lin, col)
                elif char == ",":
                    return (TOKEN.virg, ",", lin, col)
                elif char == ".":
                    return (TOKEN.pto, ".", lin, col)
                elif char == ";":
                    return (TOKEN.ptoVirg, ";", lin, col)
                elif char == "+":
                    return TOKEN.mais, "+", lin, col
                elif char == "-":
                    return TOKEN.menos, "-", lin, col
                elif char == "*":
                    return TOKEN.multiplica, "*", lin, col
                elif char == "/":
                    estado = 9
                elif char == "%":
                    return TOKEN.porcent, "%", lin, col
                elif char == "<":
                    estado = 5
                elif char == ">":
                    estado = 6
                elif char == "=":
                    estado = 7
                elif char == "!":
                    estado = 8
                elif char == "\0":
                    return (TOKEN.eof, "<eof>", lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 2:
                if char.isalnum() or char == "_":
                    estado = 2
                elif char in EXCLUDED_CHARS or char in BROKEN_CHARS:
                    self.unget_char(char)
                    return (TOKEN.reservada(lexema), lexema, lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 3:
                if char.isnumeric():
                    estado = 3
                elif char in EXCLUDED_CHARS or char in BROKEN_CHARS:
                    self.unget_char(char)
                    return (TOKEN.num, lexema, lin, col)
                else:
                    return (TOKEN.erro, lexema, lin, col)

            # TODO: Atulizar caso seja necessário utilizar o caractere de escape '\'
            elif estado == 4:
                if char == '"':
                    return (TOKEN.string, lexema, lin, col)

            elif estado == 5:
                if char == "=":
                    return (TOKEN.menorIgual, "<=", lin, col)
                else:
                    return (TOKEN.menor, "<", lin, col)

            elif estado == 6:
                if char == "=":
                    return (TOKEN.maiorIgual, ">=", lin, col)
                else:
                    return (TOKEN.maior, ">", lin, col)

            elif estado == 7:
                if char == "=":
                    return (TOKEN.igual, "==", lin, col)
                else:
                    return (TOKEN.atrib, "=", lin, col)

            elif estado == 8:
                if char == "=":
                    return (TOKEN.diferente, "!=", lin, col)
                else:
                    return (TOKEN.NOT, "!", lin, col)

            elif estado == 9:
                if char == "/":
                    # index - 2 por causa das 2 /
                    self.index -= 2
                    self.trash_comments(self.index)
                    lin = self.linha
                    col = 1
                    estado = 1
                else:
                    return TOKEN.divide, "/", lin, col

            char = self.get_char()


if __name__ == "__main__":
    path = PATH_FILE
    if len(sys.argv) <= 1:
        print("Uso: python3 seu_script.py <arquivo>")
    else:
        path = sys.argv[1]
        lex = Lexical(path)

        while not lex.end_of_file():
            tok = lex.get_token()
            lex.print_token(tok)
