grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text[1:]);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text[1:]);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    elif tk == self.STRING_ERROR:
        result = super().emit();
        # Extract the non-ASCII character from the string
        text = result.text[1:]  # Remove opening quote
        for char in text:
            if ord(char) > 127:  # Find first non-ASCII character
                raise ErrorToken(char);
        raise ErrorToken(result.text);  # Fallback
    elif tk == self.STRINGLIT:
        result = super().emit()
        result.text = result.text[1:-1]  
        return result
    else:
        return super().emit();
}

options{
    language=Python3;
}

// ========== PROGRAM STRUCTURE ==========
program: decllist EOF ;
decllist: decl decllist | ;
decl: constdecl | funcdecl ;

// ========== DECLARATIONS ==========
constdecl: CONST ID typeanno ASSIGN expr SEMI ;
funcdecl: FUNC ID LPAREN paramlist RPAREN ARROW type body ;

// ========== PARAMETERS ==========
paramlist: paramprime | ;
paramprime: param COMMA paramprime | param ;
param: ID COLON type ;

// ========== TYPE SYSTEM ==========
type: primetype | arraytype ;
primetype: INT | FLOAT | BOOL | STRING | VOID ;
arraytype: LBRACK type SEMI INTLIT RBRACK ;

// ========== FUNCTION BODY ==========
body: LBRACE stmtlist RBRACE ;

// ========== STATEMENTS ==========
stmtlist: stmt stmtlist | ;
stmt: vardecl | assignstmt | ifstmt | whilestmt | forstmt 
    | breakstmt | contstmt | returnstmt | exprstmt | blockstmt | SEMI ;

vardecl: LET ID typeanno ASSIGN expr SEMI ;
assignstmt: lvalue ASSIGN expr SEMI ;
ifstmt: IF LPAREN expr RPAREN blockstmt elselist ;
whilestmt: WHILE LPAREN expr RPAREN blockstmt ;
forstmt: FOR LPAREN ID IN expr RPAREN blockstmt ;
breakstmt: BREAK SEMI ;
contstmt: CONTINUE SEMI ;
returnstmt: RETURN expropt SEMI ;
exprstmt: expr SEMI ;
blockstmt: LBRACE stmtlist RBRACE ;

// ========== OPTIONAL PARTS ==========
typeanno: COLON type | ;
expropt: expr | ;
elselist: ELSE IF LPAREN expr RPAREN blockstmt elselist | ELSE blockstmt | ;

// ========== LVALUE ==========
lvalue: ID | arrayaccess | lvalue LBRACK expr RBRACK ;

// ========== EXPRESSIONS ==========
expr: pipeexpr ;

pipeexpr: orexpr pipepart ;
pipepart: PIPE pipecall pipepart | ;
pipecall: func_id | func_id LPAREN exprlist RPAREN ;

orexpr: andexpr orpart ;
orpart: OR andexpr orpart | ;

andexpr: eqexpr andpart ;
andpart: AND eqexpr andpart | ;

eqexpr: relexpr eqpart ;
eqpart: eqop relexpr eqpart | ;
eqop: EQ | NEQ ;

relexpr: addexpr relpart ;
relpart: relop addexpr relpart | ;
relop: LT | LE | GT | GE ;

addexpr: mulexpr addpart ;
addpart: addop mulexpr addpart | ;
addop: PLUS | MINUS ;

mulexpr: unaryexpr mulpart ;
mulpart: mulop unaryexpr mulpart | ;
mulop: MUL | DIV | MOD ;

unaryexpr: unaryop unaryexpr | primaryexpr ;
unaryop: NOT | PLUS | MINUS ;

primaryexpr: literal | arrayaccess | funcall | ID | arraylit | subexpr ;

// ========== SPECIFIC EXPRESSIONS ==========
literal: INTLIT | FLOATLIT | STRINGLIT | TRUE | FALSE ;
arrayaccess: ID accesspart ;
accesspart: LBRACK expr RBRACK accesspart | LBRACK expr RBRACK ;
func_id: ID | INT | FLOAT | BOOL | STRING ;
funcall: func_id LPAREN exprlist RPAREN ;
arraylit: LBRACK exprlist RBRACK ;
subexpr: LPAREN expr RPAREN ;

// ========== EXPRESSION LISTS ==========
exprlist: exprprime | ;
exprprime: expr COMMA exprprime | expr ;

// ========== KEYWORDS ==========
BOOL: 'bool';
BREAK: 'break';
CONST: 'const';
CONTINUE: 'continue';
ELSE: 'else';
FALSE: 'false';
FLOAT: 'float';
FOR: 'for';
FUNC: 'func';
IF: 'if';
IN: 'in';
INT: 'int';
LET: 'let';
RETURN: 'return';
STRING: 'string';
TRUE: 'true';
VOID: 'void';
WHILE: 'while';



// ========== OPERATORS ==========
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
AND: '&&';
OR: '||';
NOT: '!';
ASSIGN: '=';
COLON: ':';
ARROW: '->';
PIPE: '>>';

// ========== SEPARATORS ==========
LPAREN: '(';
RPAREN: ')';
LBRACK: '[';
RBRACK: ']';
LBRACE: '{';
RBRACE: '}';
COMMA: ',';
SEMI: ';';
DOT: '.';
// ========== IDENTIFIERS ==========
ID: [a-zA-Z_][a-zA-Z0-9_]*;
// ========== LITERALS ==========
INTLIT: [0-9]+;
FLOATLIT: [0-9]+ '.' [0-9]*([eE] [+-]?[0-9]+)? ;
STRINGLIT: '"' ( VALID_CHAR | ESC_SEQ )* '"';
fragment VALID_CHAR: [\u0020-\u0021\u0023-\u005B\u005D-\u007E];  
fragment ESC_SEQ: '\\' [tnr"\\];

// ========== COMMENTS ==========
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' (BLOCK_COMMENT|.)*? '*/' -> skip;


// ========== WHITESPACE ==========
WS: [ \t\r\n]+ -> skip;

// ========== ERROR HANDLING ==========
ILLEGAL_ESCAPE: '"' ( VALID_CHAR | ESC_SEQ )* '\\' ~[tnr"\\];
STRING_ERROR: '"' ( VALID_CHAR | ESC_SEQ )* ~[\u0020-\u007E];
UNCLOSE_STRING: '"' ( VALID_CHAR | ESC_SEQ )*;  
ERROR_CHAR: .;
