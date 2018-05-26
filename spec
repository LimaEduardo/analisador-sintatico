compilationUnit ::= [package qualifiedIdentifier ;] {import qualifiedIdentifier ;} {typeDeclaration} EOF

qualifiedIdentifier ::= <identifier> {. <identifier>}

typeDeclaration ::= modifiers classDeclaration

modifiers ::= {public | protected | private | static | abstract}

classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody

classBody ::= { {modifiers memberDecl} }

memberDecl ::= <identifier> formalParameters block
| (void | type) <identifier> formalParameters (block | ;)
| type variableDeclarators ;

block ::= { {blockStatement} }

blockStatement ::= localVariableDeclarationStatement
| statement

statement ::= block
| <identifier> : statement
| if parExpression statement [else statement]
| while parExpression statement
| return [expression] ;
| ;
| statementExpression ;

formalParameters ::= ( [formalParameter {, formalParameter}] )

formalParameter ::= type <identifier>

parExpression ::= ( expression )

localVariableDeclarationStatement ::= type variableDeclarators ;

variableDeclarators ::= variableDeclarator {, variableDeclarator}

variableDeclarator ::= <identifier> [= variableInitializer]

variableInitializer ::= arrayInitializer | expression

arrayInitializer ::= { [variableInitializer {, variableInitializer}] }

arguments ::= ( [expression {, expression}] )

type ::= referenceType | basicType

basicType ::= boolean | char | int

referenceType ::= basicType [ ] {[ ]}
| qualifiedIdentifier {[ ]}

statementExpression ::= expression

expression ::= assignmentExpression

assignmentExpression ::= conditionalAndExpression [(= | +=) assignmentExpression]

conditionalAndExpression ::= equalityExpression {&& equalityExpression}

equalityExpression ::= relationalExpression {== relationalExpression}

relationalExpression ::= additiveExpression [(> | <=) additiveExpression | instanceof referenceType] additiveExpression ::= multiplicativeExpression {(+ | -) multiplicativeExpression}

multiplicativeExpression ::= unaryExpression {* unaryExpression}

unaryExpression ::= ++ unaryExpression
| - unaryExpression
| simpleUnaryExpression

simpleUnaryExpression ::= ! unaryExpression
| ( basicType ) unaryExpression
| ( referenceType ) simpleUnaryExpression
| postfixExpression

postfixExpression ::= primary {selector} {--}

selector ::= . qualifiedIdentifier [arguments]
| [ expression ]

primary ::= parExpression
| this [arguments]
| super (arguments | . <identifier> [arguments])
| literal
| new creator
| qualifiedIdentifier [arguments]

creator ::= (basicType | qualifiedIdentifier)
| arguments
| [ ] {[ ]} [arrayInitializer]
| newArrayDeclarator )

newArrayDeclarator ::= [ expression ] {[ expression ]} {[ ]}

literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null