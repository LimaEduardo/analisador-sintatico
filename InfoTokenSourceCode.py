import sys
from pathlib import Path

def geraInfoToken():
    arquivo = Path("tabelaDeTokens")
    if arquivo.exists():
        arquivo = open("tabelaDeTokens", "r")
        linhas = arquivo.readlines()
        del linhas[0:3]
        for index in range(len(linhas)):
            linhas[index] = linhas[index].split("|")
            del linhas[index][0]
        del linhas[-1]
        infoToken = []
        for linha in linhas:
            nomeToken = linha[3].strip()
            linhaToken = linha[1].strip()
            colunaToken = linha[2].strip()
            infoToken.append([nomeToken,linhaToken,colunaToken])
        return infoToken

