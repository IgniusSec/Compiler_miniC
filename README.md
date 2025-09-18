# Compiler_miniC

A compiler prototype for an adaptation of C lang

## Gramática:

Program -> LAMBDA
| Function Program
Function -> Type ident ( ArgList ) CompoundStmt
ArgList -> Arg
| ArgList , Arg
Arg -> Type IdentArg
IdentArg -> ident OpcIdentArg
OpcIdentArg -> LAMBDA
| [ ]
Declaration -> Type IdentList ;
Type -> int
| float
| char
IdentList -> IdentDeclar RestoIdentList
RestoIdentList -> LAMBDA
| , IdentList
IdentDeclar -> ident OpcIdentDeclar
OpcIdentDeclar -> LAMBDA
| [ intNumber ]
Stmt -> ForStmt
| WhileStmt
| Expr ;
| IfStmt
| CompoundStmt
| Declaration
| break ;
| continue ;
| return Expr ;
| ;
ForStmt -> for ( Expr ; OptExpr ; OptExpr ) Stmt
OptExpr -> Expr
| LAMBDA
WhileStmt -> while ( Expr ) Stmt
IfStmt -> if ( Expr ) Stmt ElsePart
ElsePart -> else Stmt
| LAMBDA
CompoundStmt -> { StmtList }
StmtList -> StmtList Stmt
| LAMBDA
Expr -> ident OpcLeft = Expr
| Rvalue
OpcLeft -> LAMBDA
| [ IndicePuro ]
IndicePuro -> intNumber
| ident
Rvalue -> Mag RestoRvalue
RestoRvalue -> Compare Mag RestoRvalue
| LAMBDA
Compare -> == | < | > | <= | >= | !=
Mag -> Term RestoMag
RestoMag -> + Term RestoMag
| - Term RestoMag
| LAMBDA
Term -> Factor RestoTerm
RestoTerm -> \* Factor RestoTerm
| / Factor RestoTerm
| % Factor RestoTerm
| LAMBDA
Factor -> ( Expr )
| - Factor
| + Factor
| Identifier
| intNumber
| floatNumber
| string
Identifier -> ident OpcIdentifier
OpcIdentfier -> LAMBDA
| [ Exp ]
