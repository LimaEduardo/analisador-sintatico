import sys
from pathlib import Path

def getArquivo(nomeArquivo):
    arquivo = Path(nomeArquivo)

    if not arquivo.exists():
        print("Arquivo não existe")
        sys.exit()
    
    arquivo = open(nomeArquivo, "r")
    linhasArquivo = arquivo.read().splitlines()
    return linhasArquivo

def organizaDados(linhasArquivo):
    indiceLinha = 0
    linhasDict = {}
    ladoDireito= ""
    while indiceLinha != len(linhasArquivo):
        linhaAtual = linhasArquivo[indiceLinha]
        if linhaAtual == "":
            indiceLinha += 1
            continue
        
        if linhaAtual[0] == "|":
            linhasDict[ladoDireito].append(linhaAtual.split("|")[1])

        if "::=" in linhaAtual:
            ladoDireito = linhaAtual.split("::=")[0]
            linhasDict[ladoDireito] = []
            linhasDict[ladoDireito].append(linhaAtual.split("::=")[1])
        
        indiceLinha += 1
    
    return linhasDict

def montaFirst(linhasDict): 
    conjuntoFirst = {}
    for expressao in linhasDict.keys():
        conjuntoFirst[expressao] = first(linhasDict[expressao])
    return conjuntoFirst

def first(expressao):
    print(expressao)
    print("")

if __name__ == "__main__" :
    linhasDict = organizaDados(getArquivo("spec"))
    conjuntoFirst = montaFirst(linhasDict)
    