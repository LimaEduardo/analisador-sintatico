from leitorDeFluxo import LeitorDeFluxo
from tipoToken import TipoToken
from error import Error

class analisadorSintatico:
    
    def __init__(self):
        self.tokens = LeitorDeFluxo("fluxoDeTokens").fluxoDeTokens      # Lista de tokens
        self.compilationUnit()
        

    def existeToken(self, i):
        if i < len(self.tokens):
            print(self.tokens[i])
        return i < len(self.tokens)

    #compilationUnit::=[package qualifiedIdentifier ;] {import qualifiedIdentifier ;} {typeDeclaration} EOF
    def compilationUnit(self):
        indice = 0;
        if not self.existeToken(indice):
            return indice
        
        if self.tokens[indice] == TipoToken.PCPackage.name:
            indice = self.qualifiedIdentifier(indice+1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name) # Token Esperado
                return indice
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
        
        if not self.existeToken(indice):
            return indice

        while self.existeToken(indice) and self.tokens[indice] == TipoToken.PCImport.name:
            indice = self.qualifiedIdentifier(indice+1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name) # Token Esperado
                return indice
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
                if not self.existeToken(indice):
                    return indice
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])

        while self.existeToken(indice):
            indice = self.typeDeclaration(indice)

        if not self.existeToken(indice):
            return indice
        Error.EsperaTokenFimArquivo("ao finalizar o arquivo")

    # qualifiedIdentifier ::= <identifier> {. <identifier>}
    def qualifiedIdentifier(self, indice):
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
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name)
            return indice
        Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        if not self.existeToken(indice + 1):
            return indice
        return indice

    # typeDeclaration ::= modifiers classDeclaration
    def typeDeclaration(self, indice):
        indice = self.modifiers(indice)
        indice = self.classDeclaration(indice)
        return indice

    # modifiers ::= {public | protected | private | static | abstract}
    def modifiers(self, indice):
        modif = [TipoToken.PCPublic.name, TipoToken.PCProtected.name, TipoToken.PCPrivate.name, TipoToken.PCStatic.name, TipoToken.PCAbstract.name]
        if not self.existeToken(indice):
            return indice
        while self.existeToken(indice) and self.tokens[indice] in modif:
            indice += 1
        return indice
 
    # classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
    def classDeclaration(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.PCClass.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.PCClass.name:
            Error.RecebeuTokenInesperado(TipoToken.PCClass.name, self.tokens[indice])
            return indice + 1
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
            return indice + 1
        indice += 1

        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("classBody") # Token Esperado
            return indice
        if self.tokens[indice] == TipoToken.PCExtends.name:
            indice = self.qualifiedIdentifier(indice + 1)
            
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("classBody") # Token Esperado
            return indice
        indice = self.classBody(indice)
        return indice

    # classBody ::= { {modifiers memberDecl} }
    def classBody(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice + 1
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        modif = [TipoToken.PCPublic.name, TipoToken.PCProtected.name, TipoToken.PCPrivate.name, TipoToken.PCStatic.name, TipoToken.PCAbstract.name]
        while self.existeToken(indice) and self.tokens[indice] != TipoToken.SepFechaChave.name:
            if self.tokens[indice] in modif:
                indice = self.modifiers(indice)
                indice = self.memberDecl(indice)
            else:
                Error.RecebeuTokenInesperado(modif, self.tokens[indice])
                indice += 1
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name) 
            return indice   
        return indice + 1  

    # memberDecl ::= <identifier> // constructor
    #                    formalParameters block
    #                | (void | type) <identifier> // method
    #                    formalParameters (block | ;)
    #                | type variableDeclarators ; // field
    def memberDecl(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("memberDecl")
            return indice

        if self.tokens[indice] == TipoToken.Variavel.name:  # CONSTRUTOR
            if self.existeToken(indice + 1) and self.tokens[indice + 1] == TipoToken.SepAbreParentese.name:
                indice += 1
                indice = self.formalParameters(indice)
                indice = self.block(indice)
                return indice

        if self.tokens[indice] == TipoToken.PCVoid.name:
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
                return indice
        else:
            indice = self.funcaoType(indice)
            if not self.existeToken(indice):                
                Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
                return indice
            if self.tokens[indice] == TipoToken.Variavel.name: # FIELD
                if self.existeToken(indice + 1) and self.tokens[indice + 1] != TipoToken.SepAbreParentese.name:
                    indice = self.variableDeclarators(indice)
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                        return indice
                    if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                        Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
                        return indice
                    return indice + 1

        # METHOD
        if self.tokens[indice] == TipoToken.Variavel.name:
            indice = self.formalParameters(indice + 1)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
            indice += 1
            return indice 
        indice = self.block(indice)
        return indice

    # block ::= { {blockStatement} }
    def block(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
            return indice

        while not self.tokens[indice] == TipoToken.SepFechaChave.name:
            indice = self.blockStatement(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
                return indice
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
            return indice
        return indice + 1
    
    # blockStatement ::= localVariableDeclarationStatement | statement
    def blockStatement(self, indice):
        if self.existeToken(indice + 1 ):
            percorreu = False

            if self.tokens[indice + 1] == TipoToken.Variavel.name:
                aux = self.qualifiedIdentifier(indice + 1)

                if self.tokens[aux] == TipoToken.SepAbreColchete.name:
                    aux = self.funcaoType(indice + 2)

                if self.tokens[aux] == TipoToken.Variavel.name:
                    percorreu = True

            elif self.ehUmBasicType(indice + 1):
                aux = self.funcaoType(indice + 1)

                if self.tokens[aux] == TipoToken.Variavel.name:
                    percorreu = True

            if percorreu:
                indice = self.localVariableDeclarationStatement(indice)
                return indice

            indice = self.statement(indice)
            return indice

        return indice + 1

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    '''def statement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("statement")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        if self.tokens[indice] == TipoToken.Variavel.name:               # <identifier>
            if not self.tokens[indice] == TipoToken.SepDoisPontos.name:
                Error.RecebeuTokenInesperado(TipoToken.SepDoisPontos.name, self.tokens[indice])
                return indice
            return self.statement(indice + 1)

        if self.tokens[indice] == TipoToken.PCIf.name:                 # if
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.PCElse.name:
                return self.statement(indice + 1)

            return indice

        if self.tokens[indice] == TipoToken.PCWhile.name:              # while
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            return indice

        if self.tokens[indice] == TipoToken.PCReturn.name:             # return
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                return indice
            if self.tokens[indice].TipoToken != TipoToken.SepPontoEVirgula:
                indice = self.expression(indice)
        
        indice = self.statementExpression(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(TipoToken.SepPontoEVirgula)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:     # ;
            Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            return indice
        return indice + 1'''

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    def statement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("statement")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        '''if self.tokens[indice] == TipoToken.Variavel.name:               # <identifier>
            if not self.tokens[indice] == TipoToken.SepDoisPontos.name:
                Error.RecebeuTokenInesperado(TipoToken.SepDoisPontos.name, self.tokens[indice])
                return indice
            return self.statement(indice + 1)'''

        if self.tokens[indice] == TipoToken.PCIf.name:                 # if
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.PCElse.name:
                return self.statement(indice + 1)

            return indice

        if self.tokens[indice] == TipoToken.PCWhile.name:              # while
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            return indice

        if self.tokens[indice] == TipoToken.PCReturn.name:             # return
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                return indice
            if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                indice = self.expression(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                    return indice
                if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                    Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
                    return indice
                indice += 1
            return indice

        if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
            indice += 1
            return indice
        indice = self.statementExpression(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken(TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:     # ;
            Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            return indice
        return indice + 1


    # formalParameters ::= ( [formalParameter {, formalParameter}] )
    def formalParameters(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice   
        indice += 1 
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            indice = self.formalParameter(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                return indice

            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice = self.formalParameter(indice + 1)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo("formalParameter")
                    return indice
                
        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
            return indice
        return indice + 1

    # formalParameter ::= type <identifier>
    def formalParameter(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("Type")
            return indice
        indice = self.funcaoType(indice)
        if not self.existeToken(indice):
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name, self.tokens[indice])
            return indice
        return indice + 1

    # parExpression ::= ( expression )
    def parExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice
        if self.tokens[indice] != TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice

        indice = self.expression(indice + 1)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
            return indice

        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
            return indice

        return indice + 1

    # localVariableDeclarationStatement ::= type variableDeclarators ;
    def localVariableDeclarationStatement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("type")
            return indice
        indice = self.funcaoType(indice)
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("variable declarators")
            return indice
        indice = self.variableDeclarators(indice) 
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
            Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])            
            return indice
        return indice + 1
            
    # variableDeclarators ::= variableDeclarator {, variableDeclarator}
    def variableDeclarators(self, indice):
        indice = self.variableDeclarator(indice)
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice += 1
            if not self.existeToken(indice):
                Error.NaoFoiPossivelLerMaisToken("variable declarator")
                return indice
            indice = self.variableDeclarator(indice)
        return indice

    # variableDeclarator ::= <identifier> [= variableInitializer]
    def variableDeclarator(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.existeToken(indice):
            return indice

        if self.tokens[indice] == TipoToken.OPRecebe.name:
            indice = self.variableInitializer(indice + 1)

        return indice 

    # variableInitializer ::= arrayInitializer | expression
    def variableInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreChave.name: 
            indice = self.arrayInitializer(indice)
            return indice
        return self.expression(indice)

    # arrayInitializer ::= { [variableInitializer {, variableInitializer}] }
    def arrayInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] != TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice
        indice = self.variableInitializer(indice + 1)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
            return indice

        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice = self.variableInitializer(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
                return indice

        if not self.tokens[indice] == TipoToken.SepFechaChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaChave.name, self.tokens[indice])
            return indice

        return indice + 1
        
    # arguments ::= ( [expression {, expression}] )
    def arguments(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreParentese.name, self.tokens[indice])
            return indice
        indice += 1
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            indice = self.expression(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepVirgula.name)
                return indice
            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice = self.expression(indice + 1)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepVirgula.name)
                    return indice
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
            return indice
        indice += 1
        return indice

    # type ::= referenceType | basicType
    def funcaoType(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("'reference type' or 'basic type'")
            return indice
        if self.ehUmBasicType(indice):
            if self.existeToken(indice + 1) and self.tokens[indice + 1]  == TipoToken.SepAbreColchete.name:
                    return self.referenceType(indice)
            return self.basicType(indice)
        return self.referenceType(indice)
        
    # basicType ::= boolean | char | int
    def basicType(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name])
            return indice
        if not self.ehUmBasicType(indice):
            Error.EsperaTokenFimArquivo([TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name])
            return indice
        return indice + 1

    # referenceType ::= basicType [ ] {[ ]} | qualifiedIdentifier {[ ]}
    def referenceType(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("basic type or qualifedIdentifier")
            return indice

        if self.ehUmBasicType(indice):
            indice += 1
            
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
                return indice

            if self.tokens[indice] != TipoToken.SepAbreColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepAbreColchete.name, self.tokens[indice])
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
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice
        return indice + 1

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
            indice = self.assignmentExpression(indice + 1)
        return indice

    # conditionalAndExpression ::= equalityExpression {&& equalityExpression}
    def conditionalAndExpression(self, indice):
        indice = self.equalityExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPAnd.name:
            indice = self.equalityExpression(indice + 1)
            if not self.existeToken(indice):
                return indice

        return indice

    # equalityExpression ::= relationalExpression {== relationalExpression}
    def equalityExpression(self, indice):
        indice = self.relationalExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPIgual.name:
            indice = self.relationalExpression(indice + 1)
            if not self.existeToken(indice):
                return indice
        return indice

    # relationalExpression ::= additiveExpression [(> | <=) additiveExpression | instanceof referenceType]
    def relationalExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("additive expression")
            return indice
        indice = self.additiveExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.OPMaior.name, TipoToken.OPMenorIgual.name ])
            return indice

        if self.tokens[indice] == TipoToken.OPMaior.name or self.tokens[indice] == TipoToken.OPMenorIgual.name: 
            indice = self.additiveExpression(indice + 1)
        elif self.tokens[indice] == TipoToken.PCInstanceOf.name:
            indice = self.referenceType(indice + 1)

        return indice

    # additiveExpression ::= multiplicativeExpression {(+ | -) multiplicativeExpression}
    def additiveExpression(self, indice):
        indice = self.multiplicativeExpression(indice)
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.OPSoma.name or self.tokens[indice] == TipoToken.OPMenos.name:
            indice = self.multiplicativeExpression(indice + 1)
            if not self.existeToken(indice):
                return indice
        return indice

    # multiplicativeExpression ::= unaryExpression {* unaryExpression}
    def  multiplicativeExpression(self, indice):
        indice = self.unaryExpression(indice)
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] == TipoToken.OpMultiplica.name:
            indice = self.unaryExpression(indice + 1)
            if not self.existeToken(indice):
                return indice
        return indice

    # unaryExpression ::= ++ unaryExpression | - unaryExpression | simpleUnaryExpression
    def unaryExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo("unaryExpression")
            return indice

        if self.tokens[indice] == TipoToken.OPIncrementa.name:
            return self.simpleUnaryExpression(indice + 1)

        if self.tokens[indice] == TipoToken.OPMenos.name:
            return self.simpleUnaryExpression(indice + 1)

        return self.simpleUnaryExpression(indice)

    # simpleUnaryExpression ::= ! unaryExpression | ( basicType ) unaryExpression 
    #                           | ( referenceType ) simpleUnaryExpression | postfixExpression
    def simpleUnaryExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OPNao.name)
            return indice

        if self.tokens[indice] == TipoToken.OPNao.name:
            return self.unaryExpression(indice + 1)

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice += 1

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo("simpleUnaryExpression")
                return indice

            if self.ehUmBasicType(indice) :
                aux = self.basicType(indice)

                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                    return indice

                if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                    indice = self.referenceType(indice)

                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                        return indice

                    if self.tokens[indice] != TipoToken.SepFechaParentese.name :
                        Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])

                    return self.simpleUnaryExpression(indice + 1)
                
                else:
                    indice = aux
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                        return indice

                    if(self.tokens[indice] != TipoToken.SepFechaParentese.name):
                        Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                    return self.unaryExpression(indice + 1)

            elif self.ehUmReferenceType(indice):
                
                indice = self.referenceType(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                    return indice

                if self.tokens[indice] != TipoToken.SepFechaParentese :
                    Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                return self.simpleUnaryExpression(indice + 1)
            else:
                return self.postfixExpression(indice + 1)

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
            Error.EsperaTokenFimArquivo(TipoToken.SepPonto.name)
            return indice
        if self.tokens[indice] == TipoToken.SepPonto.name:
            indice = self.qualifiedIdentifier(indice + 1)

            if not self.existeToken(indice):
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
            return indice

        if self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.expression(indice + 1)

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
                return indice

            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice
            return indice + 1
        return indice

    # primary ::= parExpression | this [arguments] | super (arguments | . <identifier> [arguments])
    #                           | literal | new creator | qualifiedIdentifier [arguments]
    def primary(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
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
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            if self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
                if not self.tokens[indice] == TipoToken.Variavel.name:
                    Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
                if not self.existeToken(indice):
                    return indice
                if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                    indice = self.arguments(indice)
                return indice
            Error.RecebeuTokenInesperado("Separador ou argumentos", self.tokens[indice] )
            return indice + 1


        if(self.eUmLiteral(indice)):          # literal
            return self.literal(indice)

        if(self.tokens[indice] == TipoToken.PCNew.name):        # New 
            return self.creator(indice + 1)

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
            Error.NaoFoiPossivelLerMaisToken("Type")
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
                Error.NaoFoiPossivelLerMaisToken("Arguments")
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice = self.newArrayDeclarator(indice)
                return indice

        elif self.eUmQualifiedIdentifier(indice):
            indice = self.qualifiedIdentifier(indice)
            
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            indice = self.newArrayDeclarator(indice)
            return indice
        Error.NaoFoiPossivelLerMaisToken("Type")
        return indice

    # newArrayDeclarator ::= [ expression ] {[ expression ]} {[ ]}
    def newArrayDeclarator(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
            return indice

        if not self.tokens[indice] == TipoToken.SepAbreColchete.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreColchete.name, self.tokens[indice])
            return indice 

        indice = self.expression(indice + 1)

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
            return indice 

        indice += 1

        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice += 1

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
                return indice

            if self.tokens[indice] == TipoToken.SepFechaColchete.name:
                indice += 1

                while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
                    indice += 1
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                        return indice
                    if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                        Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                        return indice
                    indice += 1
                return indice

            indice = self.expression(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                return indice

            if self.tokens[indice]  != TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice

        return indice + 1
        

    # literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null
    def literal(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name])
            return indice
        literais = [TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name]
        if self.tokens[indice] in literais:
            return indice + 1
        Error.EsperaTokenFimArquivo([TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name])
        return indice + 1

    #################### FUNÇÕES AUXILIARES ####################
    def ehUmType(self, indice):
        return self.ehUmBasicType(indice) or self.ehUmReferenceType(indice)

    def ehUmBasicType(self,indice):
        tiposBasicos = [TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name]
        if self.existeToken(indice) and self.tokens[indice] in tiposBasicos:
            return True
        return False

    def ehUmReferenceType(self,indice):
        if self.existeToken(indice) and self.ehUmBasicType(indice):
            indice += 1
            if self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice += 1
            if self.existeToken(indice) and self.tokens[indice] == TipoToken.SepFechaColchete.name:
                return True
        elif self.existeToken(indice) and self.ehUmQualifiedIdentifier(indice):
            return True
        else : 
            return False

    def ehUmQualifiedIdentifier(self,indice):
        return self.existeToken(indice) and self.tokens[indice] == TipoToken.Variavel.name

    def eUmLiteral(self,indice):
        if((self.tokens[indice] == TipoToken.Int.name) or (self.tokens[indice] == TipoToken.Char.name) or
           (self.tokens[indice] == TipoToken.String.name) or (self.tokens[indice] == TipoToken.PCTrue.name) or
           (self.tokens[indice] == TipoToken.PCFalse.name) or (self.tokens[indice] == TipoToken.PCNull.name)):
            return True
        return False

if __name__ == "__main__":
    analisador = analisadorSintatico()