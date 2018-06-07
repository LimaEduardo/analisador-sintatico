from leitorDeFluxo import LeitorDeFluxo
from tipoToken import TipoToken
from error import Error
from InfoTokenSourceCode import geraInfoToken

class analisadorSintatico:
    
    def __init__(self):
        self.tokens = LeitorDeFluxo("fluxoDeTokens").fluxoDeTokens      # Lista de tokens
        self.infoTokens = geraInfoToken()
        self.compilationUnit()
        

    def existeToken(self, i):
        if i < len(self.tokens):
            print(self.tokens[i])
        return i < len(self.tokens)

    #compilationUnit::=[package qualifiedIdentifier ;] {import qualifiedIdentifier ;} {typeDeclaration} EOF
    def compilationUnit(self):  #
        indice = 0;
        if not self.existeToken(indice):
            return indice
        
        if self.tokens[indice] == TipoToken.PCPackage.name:
            indice += 1
            indice = self.qualifiedIdentifier(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name) # Token Esperado
                return indice
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])
        
        if not self.existeToken(indice):
            return indice

        while self.existeToken(indice) and self.tokens[indice] == TipoToken.PCImport.name:
            indice += 1
            indice = self.qualifiedIdentifier(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name) # Token Esperado
                return indice
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])

        while self.existeToken(indice):
            indice = self.typeDeclaration(indice)

        if not self.existeToken(indice):
            return indice
        Error.EsperaTokenFimArquivo(self.infoTokens[indice],"ao finalizar o arquivo")

    # qualifiedIdentifier ::= <identifier> {. <identifier>}
    def qualifiedIdentifier(self, indice):  #
        if not self.existeToken(indice):
            return indice
        while self.existeToken(indice) and self.tokens[indice] == TipoToken.Variavel.name:
            indice += 1
            if not self.existeToken(indice):
                return indice
            if self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
            else:
                return indice
        if not self.existeToken(indice):
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name)
            return indice
        Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
        if not self.existeToken(indice + 1):
            return indice
        return indice

    # typeDeclaration ::= modifiers classDeclaration
    def typeDeclaration(self, indice):  #
        indice = self.modifiers(indice)
        indice = self.classDeclaration(indice)
        return indice

    # modifiers ::= {public | protected | private | static | abstract}
    def modifiers(self, indice):    #
        modif = [TipoToken.PCPublic.name, TipoToken.PCProtected.name, TipoToken.PCPrivate.name, TipoToken.PCStatic.name, TipoToken.PCAbstract.name]
        if not self.existeToken(indice):
            return indice
        while self.existeToken(indice) and self.tokens[indice] in modif:
            indice += 1
        return indice
 
    # classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
    def classDeclaration(self, indice):     #
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.PCClass.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.PCClass.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.PCClass.name, self.tokens[indice])
            indice += 1
            return indice
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.Variavel.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
            indice += 1
            return indice
        indice += 1

        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"classBody") # Token Esperado
            return indice
        if self.tokens[indice] == TipoToken.PCExtends.name:
            indice += 1
            indice = self.qualifiedIdentifier(indice)
            
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"classBody") # Token Esperado
            return indice
        indice = self.classBody(indice)
        return indice

    # classBody ::= { {modifiers memberDecl} }
    def classBody(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreChave.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice + 1
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreChave.name)
            return indice
        modif = [TipoToken.PCPublic.name, TipoToken.PCProtected.name, TipoToken.PCPrivate.name, TipoToken.PCStatic.name, TipoToken.PCAbstract.name]
        while self.existeToken(indice) and self.tokens[indice] != TipoToken.SepFechaChave.name:
            if self.tokens[indice] in modif:
                indice = self.modifiers(indice)
            else:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],modif, self.tokens[indice])
                indice += 1
                continue
            indice = self.memberDecl(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name) 
            return indice   
        return indice + 1

    # memberDecl ::= <identifier> // constructor
    #                    formalParameters block
    #                | (void | type) <identifier> // method
    #                    formalParameters (block | ;)
    #                | type variableDeclarators ; // field
    def memberDecl(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"memberDecl")
            return indice

        if self.tokens[indice] == TipoToken.Variavel.name:  # CONSTRUTOR
            indice += 1
            if self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice += 1
                indice = self.formalParameters(indice)
                indice = self.block(indice)
                return indice

        if self.tokens[indice] == TipoToken.PCVoid.name:
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.Variavel.name)
                return indice
        else:
            indice = self.funcaoType(indice)
            if not self.existeToken(indice):                
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.Variavel.name)
                return indice
            if self.tokens[indice] == TipoToken.Variavel.name: # FIELD
                indice += 1
                if self.existeToken(indice) and self.tokens[indice] != TipoToken.SepAbreParentese.name:
                    indice = self.variableDeclarators(indice)
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
                        return indice
                    if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                        Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])
                        return indice
                    indice += 1
                    return indice

        # METHOD
        if self.tokens[indice] == TipoToken.Variavel.name:
            indice += 1
            indice = self.formalParameters(indice)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
            indice += 1
            return indice 
        indice = self.block(indice)
        return indice

    # block ::= { {blockStatement} }
    def block(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name)
            return indice

        while not self.tokens[indice] == TipoToken.SepFechaChave.name:
            indice = self.blockStatement(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name)
                return indice
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name)
            return indice
        indice += 1
        return indice
    
    # blockStatement ::= localVariableDeclarationStatement | statement
    def blockStatement(self, indice): #
        aux = indice 
        if self.existeToken(aux):
            percorreu = False

            if self.tokens[aux] == TipoToken.Variavel.name:
                teste = aux
                aux = self.qualifiedIdentifier(aux)

                if(self.tokens[aux] == TipoToken.SepAbreColchete.name):
                    aux = self.funcaoType(teste)

                if(self.tokens[aux] == TipoToken.Variavel.name):
                    percorreu = True

            elif self.ehUmBasicType(aux):
                aux = self.funcaoType(aux)
                if(self.tokens[aux] == TipoToken.Variavel.name):
                    percorreu = True

            if(percorreu):
                indice = self.localVariableDeclarationStatement(indice)
                return indice

            indice = self.statement(indice)
            return indice
        return indice

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    '''def statement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"statement")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        if self.tokens[indice] == TipoToken.Variavel.name:               # <identifier>
            if not self.tokens[indice] == TipoToken.SepDoisPontos.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepDoisPontos.name, self.tokens[indice])
                return indice
            indice += 1
            return self.statement(indice)

        if self.tokens[indice] == TipoToken.PCIf.name:                 # if
            indice += 1
            indice = self.parExpression(indice)
            indice += 1
            indice = self.statement(indice)
            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.PCElse.name:
                indice += 1
                return self.statement(indice)

            return indice

        if self.tokens[indice] == TipoToken.PCWhile.name:              # while
            indice += 1
            indice = self.parExpression(indice)
            indice += 1
            indice = self.statement(indice)
            return indice

        if self.tokens[indice] == TipoToken.PCReturn.name:             # return
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
                return indice
            if self.tokens[indice].TipoToken != TipoToken.SepPontoEVirgula:
                indice = self.expression(indice)
        
        indice = self.statementExpression(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],TipoToken.SepPontoEVirgula)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:     # ;
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            return indice
        indice += 1
        return indice'''

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    def statement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"statement")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        '''if self.tokens[indice] == TipoToken.Variavel.name:               # <identifier>
            if not self.tokens[indice] == TipoToken.SepDoisPontos.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepDoisPontos.name, self.tokens[indice])
                return indice
            indice += 1
            return self.statement(indice)'''

        if self.tokens[indice] == TipoToken.PCIf.name:                 # if
            indice += 1
            indice = self.parExpression(indice)
            indice += 1
            indice = self.statement(indice)
            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.PCElse.name:
                indice += 1
                return self.statement(indice)

            return indice

        if self.tokens[indice] == TipoToken.PCWhile.name:              # while
            indice += 1
            indice = self.parExpression(indice)
            indice += 1
            indice = self.statement(indice)
            return indice

        if self.tokens[indice] == TipoToken.PCReturn.name:             # return
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
                return indice
            if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                indice = self.expression(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
                    return indice
                if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                    Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])
                    return indice
                indice += 1
            return indice

        if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
            indice += 1
            return indice
        indice = self.statementExpression(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:     # ;
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            return indice
        indice += 1
        return indice


    # formalParameters ::= ( [formalParameter {, formalParameter}] )
    def formalParameters(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice   
        indice += 1 
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            indice = self.formalParameter(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
                return indice

            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice += 1
                indice = self.formalParameter(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(self.infoTokens[indice],"formalParameter")
                    return indice
                
        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaParentese.name, self.tokens[indice])
            return indice
        indice += 1
        return indice

    # formalParameter ::= type <identifier>
    def formalParameter(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"Type")
            return indice
        indice = self.funcaoType(indice)
        if not self.existeToken(indice):
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
            return indice
        indice += 1
        return indice

    # parExpression ::= ( expression )
    def parExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreParentese.name)
            return indice
        if self.tokens[indice] != TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice

        indice += 1
        indice = self.expression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
            return indice

        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaParentese.name, self.tokens[indice])
            return indice

        indice += 1
        return indice

    # localVariableDeclarationStatement ::= type variableDeclarators ;
    def localVariableDeclarationStatement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"type")
            return indice
        indice = self.funcaoType(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"variable declarators")
            return indice
        indice = self.variableDeclarators(indice) 
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepPontoEVirgula.name, self.tokens[indice])            
            return indice
        indice += 1
        return indice
            
    # variableDeclarators ::= variableDeclarator {, variableDeclarator}
    def variableDeclarators(self, indice):
        indice = self.variableDeclarator(indice)
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice += 1
            if not self.existeToken(indice):
                Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"variable declarator")
                return indice
            indice = self.variableDeclarator(indice)
        return indice

    # variableDeclarator ::= <identifier> [= variableInitializer]
    def variableDeclarator(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.Variavel.name)
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.existeToken(indice):
            return indice

        if self.tokens[indice] == TipoToken.OPRecebe.name:
            indice += 1
            indice = self.variableInitializer(indice)

        return indice 

    # variableInitializer ::= arrayInitializer | expression
    def variableInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreChave.name)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreChave.name: 
            indice = self.arrayInitializer(indice)
            return indice
        return self.expression(indice)

    # arrayInitializer ::= { [variableInitializer {, variableInitializer}] }
    def arrayInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] != TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice
        indice += 1
        indice = self.variableInitializer(indice)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name)
            return indice

        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice += 1
            indice = self.variableInitializer(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaChave.name)
                return indice

        if not self.tokens[indice] == TipoToken.SepFechaChave.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaChave.name, self.tokens[indice])
            return indice

        indice += 1
        return indice
        
    # arguments ::= ( [expression {, expression}] )
    def arguments(self, indice):    #
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            indice = self.expression(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepVirgula.name)
                return indice
            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice += 1
                indice = self.expression(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepVirgula.name)
                    return indice

        indice += 1
        return indice

    # type ::= referenceType | basicType
    def funcaoType(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"'reference type' or 'basic type'")
            return indice
        if self.ehUmBasicType(indice):
            indice += 1
            if self.existeToken(indice) and self.tokens[indice]  == TipoToken.SepAbreColchete.name:
                return self.referenceType(indice)
            return self.basicType(indice)
        return self.referenceType(indice)
        
    # basicType ::= boolean | char | int
    def basicType(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],[TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name])
            return indice
        if not self.ehUmBasicType(indice):
            Error.RecebeuTokenInesperado(self.infoTokens[indice],[TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name], self.tokens[indice])
            return indice
        indice += 1
        return indice

    # referenceType ::= basicType [ ] {[ ]} | qualifiedIdentifier {[ ]}
    def referenceType(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"basic type or qualifedIdentifier")
            return indice

        if self.ehUmBasicType(indice):
            indice += 1
            
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreColchete.name)
                return indice

            if self.tokens[indice] != TipoToken.SepAbreColchete.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreColchete.name, self.tokens[indice])
                return indice 

        else:
            indice = self.qualifiedIdentifier(indice)
            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] != TipoToken.SepAbreColchete.name:
                return indice 
        
        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaColchete.name)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice
        indice += 1
        return indice

    # statementExpression ::= expression // but must have side-effect, eg i++
    def statementExpression(self, indice):
        return self.expression(indice)

    # expression ::= assignmentExpression
    def expression(self, indice):
        return self.assignmentExpression(indice)

    # assignmentExpression ::= conditionalAndExpression [(= | +=) assignmentExpression]
    def assignmentExpression(self, indice):
        indice = self.conditionalAndExpression(indice)
        if not self.existeToken(indice):
            return indice
        if self.tokens[indice] == TipoToken.OPRecebe.name or self.tokens[indice] == TipoToken.OPSomaERecebe.name: 
            indice += 1
            indice = self.assignmentExpression(indice)
        return indice

    # conditionalAndExpression ::= equalityExpression {&& equalityExpression}
    def conditionalAndExpression(self, indice):
        indice = self.equalityExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPAnd.name:
            indice += 1
            indice = self.equalityExpression(indice)
            if not self.existeToken(indice):
                return indice

        return indice

    # equalityExpression ::= relationalExpression {== relationalExpression}
    def equalityExpression(self, indice):
        indice = self.relationalExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPIgual.name:
            indice += 1
            indice = self.relationalExpression(indice)
            if not self.existeToken(indice):
                return indice
        return indice

    # relationalExpression ::= additiveExpression [(> | <=) additiveExpression | instanceof referenceType]
    def relationalExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"additive expression")
            return indice
        indice = self.additiveExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],[TipoToken.OPMaior.name, TipoToken.OPMenorIgual.name ])
            return indice

        if self.tokens[indice] == TipoToken.OPMaior.name or self.tokens[indice] == TipoToken.OPMenorIgual.name: 
            indice += 1
            indice = self.additiveExpression(indice)
        elif self.tokens[indice] == TipoToken.PCInstanceOf.name:
            indice += 1
            indice = self.referenceType(indice)

        return indice

    # additiveExpression ::= multiplicativeExpression {(+ | -) multiplicativeExpression}
    def additiveExpression(self, indice):
        indice = self.multiplicativeExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPSoma.name or self.tokens[indice] == TipoToken.OPMenos.name:
            indice += 1
            indice = self.multiplicativeExpression(indice)
            if not self.existeToken(indice):
                return indice
        return indice

    # multiplicativeExpression ::= unaryExpression {* unaryExpression}
    def  multiplicativeExpression(self, indice):
        indice = self.unaryExpression(indice)
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] == TipoToken.OpMultiplica.name:
            indice += 1
            indice = self.unaryExpression(indice)
            if not self.existeToken(indice):
                return indice
        return indice

    # unaryExpression ::= ++ unaryExpression | - unaryExpression | simpleUnaryExpression
    def unaryExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],"unaryExpression")
            return indice

        if self.tokens[indice] == TipoToken.OPIncrementa.name:
            indice += 1
            return self.simpleUnaryExpression(indice)

        if self.tokens[indice] == TipoToken.OPMenos.name:
            indice += 1
            return self.simpleUnaryExpression(indice)

        return self.simpleUnaryExpression(indice)

    # simpleUnaryExpression ::= ! unaryExpression | ( basicType ) unaryExpression 
    #                           | ( referenceType ) simpleUnaryExpression | postfixExpression
    def simpleUnaryExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.OPNao.name)
            return indice

        if self.tokens[indice] == TipoToken.OPNao.name:
            indice += 1
            return self.unaryExpression(indice)

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice += 1

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],"simpleUnaryExpression")
                return indice

            if self.ehUmBasicType(indice) :
                aux = self.basicType(indice)

                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
                    return indice

                if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                    indice = self.referenceType(indice)

                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
                        return indice

                    if self.tokens[indice] != TipoToken.SepFechaParentese.name :
                        Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaParentese.name, self.tokens[indice])

                    indice += 1
                    return self.simpleUnaryExpression(indice)
                
                else:
                    indice = aux
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
                        return indice

                    if(self.tokens[indice] != TipoToken.SepFechaParentese.name):
                        Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaParentese.name, self.tokens[indice])
                    indice += 1
                    return self.unaryExpression(indice)

            elif self.ehUmReferenceType(indice):
                
                indice = self.referenceType(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaParentese.name)
                    return indice

                if self.tokens[indice] != TipoToken.SepFechaParentese :
                    Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaParentese.name, self.tokens[indice])
                indice += 1
                return self.simpleUnaryExpression(indice)
            else:
                indice += 1
                return self.postfixExpression(indice)

        indice = self.postfixExpression(indice)
        return indice

    # postfixExpression ::= primary {selector} {--}
    def postfixExpression(self, indice):
        indice = self.primary(indice) 
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] == TipoToken.SepPonto.name or self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.selector(indice)
            if not self.existeToken(indice):
                return indice

        while self.tokens[indice] == TipoToken.OPDecrementa.name:
            indice += 1
            if not self.existeToken(indice):
                return indice
        return indice

    # selector ::= . qualifiedIdentifier [arguments] | [ expression ]
    def selector(self, indice): #
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepPonto.name)
            return indice
        if self.tokens[indice] == TipoToken.SepPonto.name:
            indice += 1
            indice = self.qualifiedIdentifier(indice)

            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
            return indice

        if self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice += 1
            indice = self.expression(indice)

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreColchete.name)
                return indice

            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice
            indice += 1
            return indice
        return indice

    # primary ::= parExpression | this [arguments] | super (arguments | . <identifier> [arguments])
    #                           | literal | new creator | qualifiedIdentifier [arguments]
    def primary(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreParentese.name)
            return indice

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:      # parExpression
            indice = self.parExpression(indice)
            return indice

        if self.tokens[indice] == TipoToken.PCThis.name:          # This
            indice += 1
            if not self.existeToken(indice):
                return indice
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice
            return indice

        if self.tokens[indice] == TipoToken.PCSuper.name:                   # Super
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreParentese.name)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            if self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
                if not self.tokens[indice] == TipoToken.Variavel.name:
                    Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.Variavel.name, self.tokens[indice])
                if not self.existeToken(indice):
                    return indice
                if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                    indice = self.arguments(indice)
                return indice
            Error.RecebeuTokenInesperado(self.infoTokens[indice],"Separador ou argumentos", self.tokens[indice] )
            indice += 1
            return indice


        if(self.eUmLiteral(indice)):          # literal
            return self.literal(indice)

        if(self.tokens[indice] == TipoToken.PCNew.name):        # New 
            indice += 1
            return self.creator(indice)

        aux = indice
        indice = self.qualifiedIdentifier(indice)               # senao Qualidifiertify

        if not self.existeToken(indice):
            return indice

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice = self.arguments(indice)
        if(aux == indice):
            indice += 1
        return indice

    # creator ::= (basicType | qualifiedIdentifier) ( arguments 
    #                                               | [ ] {[ ]} [arrayInitializer] 
    #                                               | newArrayDeclarator )
    def creator(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"Type")
            return indice

        if self.ehUmType(indice):
            if self.ehUmReferenceType(indice):
                indice = self.referenceType(indice)

                if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                    indice = self.arguments(indice)
                    return indice
                indice = self.arrayInitializer(indice)
                return indice 
            indice = self.basicType(indice)

            if not self.existeToken(indice):
                Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"Arguments")
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice = self.newArrayDeclarator(indice)
                return indice

        elif self.ehUmQualifiedIdentifier(indice):
            indice = self.qualifiedIdentifier(indice)
            
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            indice = self.newArrayDeclarator(indice)
            return indice
        Error.NaoFoiPossivelLerMaisToken(self.infoTokens[indice],"Type")
        return indice

    # newArrayDeclarator ::= [ expression ] {[ expression ]} {[ ]}
    def newArrayDeclarator(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreColchete.name)
            return indice

        if not self.tokens[indice] == TipoToken.SepAbreColchete.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepAbreColchete.name, self.tokens[indice])
            return indice 

        indice += 1
        indice = self.expression(indice)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreColchete.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
            Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaColchete.name, self.tokens[indice])
            return indice 

        indice += 1

        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice += 1

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepAbreColchete.name)
                return indice

            if self.tokens[indice] == TipoToken.SepFechaColchete.name:
                indice += 1

                while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
                    indice += 1
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaColchete.name)
                        return indice
                    if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                        Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaColchete.name, self.tokens[indice])
                        return indice
                    indice += 1
                return indice

            indice = self.expression(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(self.infoTokens[indice],TipoToken.SepFechaColchete.name)
                return indice

            if self.tokens[indice]  != TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(self.infoTokens[indice],TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice

        indice += 1
        return indice
        

    # literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null
    def literal(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(self.infoTokens[indice],[TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name])
            return indice
        literais = [TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name]
        if self.tokens[indice] in literais:
            indice += 1
            return indice
        Error.EsperaTokenFimArquivo(self.infoTokens[indice],[TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name])
        indice += 1
        return indice

    #################### FUNÇÕES AUXILIARES ####################
    def ehUmType(self, indice):
        return self.ehUmBasicType(indice) or self.ehUmReferenceType(indice)

    def ehUmBasicType(self,indice):
        tiposBasicos = [TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name]
        if self.existeToken(indice) and self.tokens[indice] in tiposBasicos:
            return True
        return False

    def ehUmReferenceType(self,indice):
        if(self.ehUmBasicType(indice)):
            indice += 1
            if not self.existeToken(indice):
                return False
            if self.tokens[indice] != TipoToken.SepAbreColchete.name:
                return False

        elif self.ehUmQualifiedIdentifier(indice):
            indice = self.qualifiedIdentifier(indice)
            if not self.existeToken(indice) or (self.tokens[indice] != TipoToken.SepAbreColchete.name):
                return True

        else:
            return False

        while self.existeToken(indice) and (self.tokens[indice] == TipoToken.SepAbreColchete.name):
            indice += 1
            if not self.existeToken(indice):
                return False

            if self.tokens[indice] != TipoToken.SepFechaColchete.name:
                return False

            indice += 1
        return True

    def ehUmQualifiedIdentifier(self,indice):
        while self.existeToken(indice) and (self.tokens[indice] == TipoToken.Variavel.name):
            indice += 1
            if not self.existeToken(indice):
                return True
            if self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
            else:
                return True
        if not self.existeToken(indice):
            return False
        return False

    def eUmLiteral(self,indice):
        if((self.tokens[indice] == TipoToken.Int.name) or (self.tokens[indice] == TipoToken.Char.name) or
           (self.tokens[indice] == TipoToken.String.name) or (self.tokens[indice] == TipoToken.PCTrue.name) or
           (self.tokens[indice] == TipoToken.PCFalse.name) or (self.tokens[indice] == TipoToken.PCNull.name)):
            return True
        return False

if __name__ == "__main__":
    analisador = analisadorSintatico()