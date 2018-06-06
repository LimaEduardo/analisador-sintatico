from leitorDeFluxo import LeitorDeFluxo
from tipoToken import TipoToken
from error import Error

class analisadorSintatico:
    
    def __init__(self):
        self.tokens = LeitorDeFluxo("fluxoDeTokens").fluxoDeTokens      # Lista de tokens
        self.compilationUnit()

    def existeToken(self, i):
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
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
        
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.PCImport.name:
            indice = self.qualifiedIdentifier(indice+1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name) # Token Esperado
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])

        while self.existeToken(indice):
            indice = self.typeDeclaration(indice)

        return indice

    # qualifiedIdentifier ::= <identifier> {. <identifier>}
    def qualifiedIdentifier(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
            return indice
        if self.tokens[indice] == TipoToken.Variavel.name:
            indice += 1
            while self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
                if self.tokens[indice] == TipoToken.Variavel.name:
                    indice += 1
                else:
                    Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        else:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
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
        while self.tokens[indice] in modif:
            indice += 1
        return indice
 

    # classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
    def classDeclaration(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.PCClass.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.PCClass.name:
            Error.RecebeuTokenInesperado(TipoToken.PCClass.name, self.tokens[indice])
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
        if not self.tokens[indice] == TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        indice += 1

        if self.tokens[indice] == TipoToken.PCExtends.name:
            indice = self.qualifiedIdentifier(indice + 1)
    
        indice = self.classBody(indice)
        return indice

    ########### REFATORAR ERROS DAQUI PRA BAIXO #######################
    # Eduardo

    # classBody ::= { {modifiers memberDecl} }
    def classBody(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
        indice += 1
        while self.tokens[indice] != TipoToken.SepFechaChave.name:
            if not self.existeToken(indice):
                return indice
            indice = self.modifiers(indice)
            indice = self.memberDecl(indice)
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

        elif self.tokens[indice] == TipoToken.PCVoid.name:
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
                return indice

        else:
            indice = self.funcaoType(indice)
            if not self.existeToken(indice):                
                Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
                return indice
            if self.tokens[indice] == TipoToken.Variavel.name: # METHOD
                if self.existeToken(indice + 1) and self.tokens[indice + 1] != TipoToken.SepAbreParentese.name:
                    indice += 1
                    indice = self.formalParameters(indice)
                    if not self.existeToken(indice):
                        Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                        return indice
                    if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                        indice = self.block(indice)
                    else:
                        indice += 1
                    return indice
            # FIELD
            indice = self.variableDeclarators(indice)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                return indice
            if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            return indice 

        if self.tokens[indice] == TipoToken.Variavel.name: # METHOD no caso do VOID
            indice = self.formalParameters(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
            indice = self.block(indice)
        else:
            indice += 1
        return indice

    # block ::= { {blockStatement} }
    def block(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
        indice += 1
        while self.tokens[indice] != TipoToken.SepFechaChave.name:
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
                return indice
            indice = self.blockStatement(indice)
        return indice + 1
    
    # blockStatement ::= localVariableDeclarationStatement | statement
    def blockStatement(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
            return indice
        if self.ehUmType: 
            indice = self.localVariableDeclarationStatement(indice)
        else:
            indice = self.statement(indice)
        return indice

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    def statement(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("statement")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        if self.tokens[indice] == TipoToken.Variavel.name:             # <identifier>
            if not self.tokens[indice] == TipoToken.SepDoisPontos.name:
                Error.RecebeuTokenInesperado(TipoToken.SepDoisPontos.name, self.tokens[indice])
                return indice
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.PCIf.name)
                return indice
            return self.statement(indice)

        if self.tokens[indice] == TipoToken.PCIf.name:                 # if
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.PCElse.name)
                return indice

            if self.tokens[indice] == TipoToken.PCElse.name:
                indice = self.statement(indice + 1)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.PCElse.name)
                    return indice

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
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name)
                    return indice
                if not self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                    Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
            else:
                return indice + 1

        if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:     # ;
            return indice + 1

        else:                                                          # statementExpression
            return self.statementExpression(indice + 1)

    # formalParameters ::= ( [formalParameter {, formalParameter}] )
    def formalParameters(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice = self.formalParameter(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
                return indice
            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice += 1
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                    return indice
                indice = self.formalParameter(indice)
            if self.tokens[indice] != TipoToken.SepFechaParentese:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
        return indice + 1

    # formalParameter ::= type <identifier>
    def formalParameter(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("Type")
            return indice
        indice = self.funcaoType(indice + 1)
        if not self.existeToken(indice):
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name)
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name, self.tokens[indice])
        return indice + 1

    # parExpression ::= ( expression )
    def parExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice = self.expression(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                indice += 1
        else:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
        return indice

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
            return indice + 1
            
    # variableDeclarators ::= variableDeclarator {, variableDeclarator}
    def variableDeclarators(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("variable declarator")
            return indice
        indice = self.variableDeclarator(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepVirgula.name)
            return indice
        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice += 1
            if not self.existeToken(indice):
                Error.NaoFoiPossivelLerMaisToken("variable declarator")
                return indice
            indice = self.variableDeclarator(indice)
        return indice + 1

    # variableDeclarator ::= <identifier> [= variableInitializer]
    def variableDeclarator(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name)
            return indice
        if self.tokens[indice] == TipoToken.Variavel.name:
            indice += 1
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OPIgual.name)
            return indice

        if self.tokens[indice] == TipoToken.OPIgual.name:
            indice += 1
            if not self.existeToken(indice):
                Error.NaoFoiPossivelLerMaisToken("variable declarator")
                return indice
            indice = self.variableInitializer(indice)
        else:
            return indice 

    # variableInitializer ::= arrayInitializer | expression
    def variableInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreChave.name: 
            indice = self.arrayInitializer(indice)
        else:
            indice = self.expression(indice)
        return indice

    # arrayInitializer ::= { [variableInitializer {, variableInitializer}] }
    def arrayInitializer(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepAbreChave.name, self.tokens[indice])
            return indice
        indice = self.variableInitializer(indice + 1)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepVirgula.name)
            return indice
        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice = self.variableInitializer(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaChave.name)
                return indice
        if not self.tokens[indice] == TipoToken.SepFechaChave.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaChave.name, self.tokens[indice])
            return indice
        indice += 1
        return indice
        
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
        if self.ehUmReferenceType(indice):
            indice = self.referenceType(indice + 1)
        elif self.ehUmBasicType(indice):
            indice = self.basicType(indice + 1)
        else:
            Error.NaoFoiPossivelLerMaisToken("'reference type' or 'basic type'")
        return indice

    # basicType ::= boolean | char | int
    def basicType(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name])
            return indice
        tiposBasicos = [TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name]
        if self.tokens[indice] not in tiposBasicos:
            return indice
        return indice + 1

    # referenceType ::= basicType [ ] {[ ]} | qualifiedIdentifier {[ ]}
    def referenceType(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("basic type or qualifedIdentifier")
            return indice

        if self.ehUmBasicType(indice):
            indice = self.basicType(indice)
            
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreColchete.name)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                return indice
            if self.tokens[indice] == TipoToken.SepFechaColchete.name:
                indice += 1
        elif self.ehUmQualifiedIdentifier(indice):
            indice = self.qualifiedIdentifier(indice)
        else:
            Error.NaoFoiPossivelLerMaisToken("basicType, qualifiedIdentifier")
            return indice

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
            return indice

        while self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice += 1
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
                return indice
            indice += 1

        return indice

    # statementExpression ::= expression // but must have side-effect, eg i++
    def statementExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("expression")
            return indice
        indice = self.expression(indice)
        return indice

    # expression ::= assignmentExpression
    def expression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("assignment expression")
            return indice
        indice = self.assignmentExpression(indice)
        return indice


    # assignmentExpression ::= conditionalAndExpression [(= | +=) assignmentExpression]
    def assignmentExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("conditional and expression")
            return indice
        indice = self.conditionalAndExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.OPRecebe.name, TipoToken.OPSomaERecebe.name ])
            return indice

        if self.tokens[indice] == TipoToken.OPRecebe.name or self.tokens[indice] == TipoToken.OPSomaERecebe.name: 
            indice = self.assignmentExpression(indice + 1)

        return indice

    # conditionalAndExpression ::= equalityExpression {&& equalityExpression}
    def conditionalAndExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("equality expression")
            return indice
        indice = self.equalityExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OPAnd.name)
            return indice

        while self.tokens[indice] == TipoToken.OPAnd.name:
            indice = self.equalityExpression(indice + 1)

        return indice

    # equalityExpression ::= relationalExpression {== relationalExpression}
    def equalityExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("relational expression")
            return indice
        indice = self.relationalExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.PCChar.name)
            return indice

        while self.tokens[indice] == TipoToken.OPIgual.name:
            indice = self.relationalExpression(indice + 1)

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
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("multiplicative expression")
            return indice
        indice = self.multiplicativeExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.OPSoma.name, TipoToken.OPMenos.name ])
            return indice

        while self.tokens[indice] == TipoToken.OPSoma.name or self.tokens[indice] == TipoToken.OPMenos.name:
            indice = self.multiplicativeExpression(indice + 1)

        return indice

    # multiplicativeExpression ::= unaryExpression {* unaryExpression}
    def  multiplicativeExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("unary expression")
            return indice
        indice = self.unaryExpression(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OpMultiplica.name)
            return indice

        while self.tokens[indice] == TipoToken.OpMultiplica.name:
            indice = self.unaryExpression(indice + 1)

        return indice

    # unaryExpression ::= ++ unaryExpression | - unaryExpression | simpleUnaryExpression
    def  unaryExpression(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OPIncrementa.name)
            return indice

        if self.tokens[indice] == TipoToken.OPIncrementa.name:
            indice = self.simpleUnaryExpression(indice + 1)
        elif self.tokens[indice] == TipoToken.OPMenos.name:
            indice = self.simpleUnaryExpression(indice + 1)
        else:
            indice = self.simpleUnaryExpression(indice)

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
                Error.NaoFoiPossivelLerMaisToken("basic type")
                return indice
            if self.ehUmBasicType(indice) and self.tokens[indice + 1] != TipoToken.SepAbreColchete.name: # ( basicType ) unaryExpression  
                indice = self.basicType(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                    return indice
                if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
                    Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                    return indice
                indice = self.unaryExpression(indice + 1)
            else:
                indice = self.referenceType(indice)
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                    return indice
                if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
                    Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                    return indice
                indice = self.simpleUnaryExpression(indice + 1)
            return indice

        return self.postfixExpression(indice)

    # postfixExpression ::= primary {selector} {--}
    def postfixExpression(self, indice):
        if not self.existeToken(indice):
            Error.NaoFoiPossivelLerMaisToken("primary")
            return indice
        indice = self.primary(indice) 
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.SepPonto.name, TipoToken.SepAbreColchete.name])
            return indice
        while self.tokens[indice] == TipoToken.SepPonto.name or self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.selector(indice)
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.OPDecrementa)
            return indice
        while self.tokens[indice] == TipoToken.OPDecrementa.name:
            indice += 1
        return indice

    # selector ::= . qualifiedIdentifier [arguments] | [ expression ]
    def selector(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.SepPonto.name)
            return indice
        if self.tokens[indice] == TipoToken.SepPonto.name:
            indice = self.qualifiedIdentifier(indice + 1)
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice + 1)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.expression(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                return indice
            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice
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

            return indice + 1

        if(self.eUmLiteral(indice)):          # literal
            indice = self.literal(indice)
            return indice
        if(self.tokens[indice] == TipoToken.PCNew.name):        # New
            indice = self.creator(indice + 1)
            return indice
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
            if self.ehUmBasicType(indice):
                indice = self.basicType(indice)
            else:
                indice = self.qualifiedIdentifier(indice)

            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepAbreParentese.name)
                return indice

            if(self.tokens[indice].TipoToken == TipoToken.SepAbreParentese.name): #arguments
                indice = self.arguments(indice)
                return indice

            if(self.tokens[indice].TipoToken == TipoToken.SepAbreColchete.name): 
                if((self.tokens[indice + 1].TipoToken == TipoToken.SepFechaColchete.name) or
                    (self.tokens[indice + 1].TipoToken == TipoToken.SepFechaChave.name)): 
                    while self.tokens[indice] == TipoToken.SepAbreColchete.name:
                        indice += 1
                        if not self.existeToken(indice):
                            Error.EsperaTokenFimArquivo(TipoToken.SepFechaParentese.name)
                            return indice
                        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                            Error.RecebeuTokenInesperado(TipoToken.SepFechaParentese.name, self.tokens[indice])
                            return indice
                        indice += 1
                    if self.tokens[indice].TipoToken == TipoToken.SepFechaChave.name:
                        indice = self.arrayInitializer(indice)
                        return indice
                    if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                        Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                        return indice
                return self.newArrayDeclarator(indice + 1)
        else:
            Error("Um type")
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
        if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
            Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
            return indice 
        indice += 1
        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.expression(indice + 1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepFechaColchete.name)
                return indice
            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error.RecebeuTokenInesperado(TipoToken.SepFechaColchete.name, self.tokens[indice])
                return indice 
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

    # literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null
    def literal(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo([TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name])
            return indice
        literais = [TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name]
        if not self.tokens[indice] in literais:
            return indice
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
    print (analisador)