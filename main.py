from lexical import Lexical
from sintatico import Sintatico
import sys


class Tradutor:
    def __init__(self, arq: str):
        self.nomeArq = arq

    def inicializa(self):
        self.lexico = Lexical(self.nomeArq)
        self.sintatico = Sintatico(self.lexico, "./compilado.py")

    def traduz(self):
        self.sintatico.program()

    def finaliza(self):
        self.arq.close()


# inicia a traducao
if __name__ == "__main__":
    if len(sys.argv) < 2:
        nome_arquivo = "example2.c"
        print(f"Não foi passado nome do arquivo, usando padrão: {nome_arquivo}\n\n")
    else:
        nome_arquivo = sys.argv[1]

    try:
        x = Tradutor(nome_arquivo)
        x.inicializa()
        x.traduz()
        x.finaliza()
    except Exception as e:
        print(e)
