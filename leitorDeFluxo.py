import sys
from pathlib import Path

class LeitorDeFluxo:
    def __init__(self, nomeArquivo):
        self.arquivo = Path(nomeArquivo)
        self.fluxoDeTokens = []

        if self.arquivo.exists():
            self.arquivo = open(nomeArquivo, "r")
            self.fluxoDeTokens = [self.getTipoTokenComVirgula(x.replace('>,','').replace('<','')) for x in self.arquivo.read().split(" ")]
            del self.fluxoDeTokens[-1]
            print (*self.fluxoDeTokens)
        else:
            print("Arquivo não existe")
            sys.exit()

    def getTipoTokenComVirgula(self, token):
        indice = token.find(',')
        if  indice != -1:
            return token[0:indice]
        else:
            return token

if __name__ == "__main__":
    LeitorDeFluxo("fluxoDeTokens")

