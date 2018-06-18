class Noh:
    nome = None
    filhos = None
    pai = None
    nivel = None
    idArvore = None

    def __init__(self,nome):
        self.nome = nome
        self.filhos = []
        self.niveis = -1

class Arvore:
    def __init__ (self):
        self.raiz = None
        self.nextId = 0
    
    def adicionaRaiz(self,noh):
        self.raiz = noh
        self.raiz.nivel  = 0
        self.raiz.idArvore = self.nextId
        self.nextId += 1
    
    def adicionaFilho(self,pai, filho):
        if(self.raiz == None):
            return
        filho.pai = pai
        filho.nivel = pai.nivel + 1
        filho.idArvore = self. nextId
        self.nextId += 1
        pai.filhos.append(filho)
    
    def percorreEmOrdem(self):
        saida = self.percorreEmOrdemRecursivo(self.raiz, "")
        return saida
    
    def percorreEmOrdemRecursivo(self, noh, saida):
        if noh == None:
            return ""
        pai = None
        if noh.pai != None:
            pai = noh.pai.idArvore
        saida += str(noh.idArvore) + " " + str(noh.nome) + " " + str(noh.nivel) + " " + str(pai) + "\n"
        if(len(noh.filhos) > 0):
            for filho in noh.filhos:
                saida = self.percorreEmOrdemRecursivo(filho, saida)
            return saida
        return saida
    
