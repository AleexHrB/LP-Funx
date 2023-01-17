

grammar funx;

root : ini* EOF ;

ini : expr
    | assig_g
    | conditional 
    | loop
    | function
    | callfunction
    ;


expr : '(' expr ')' #Bracket
    | '!' expr #BinaryExpr
    | <assoc=right> expr '^' expr #Expression
    | expr ('*' | '/' | '%') expr #Expression
    | expr ('+' | '-') expr #Expression
    | '-'expr #BinaryExpr
    | expr ('>' | '<' | '>=' | '<=') expr #Expression 
    | expr ('=' | '!=') expr #Expression
    | expr '&&' expr #Expression
    | expr '||' expr #Expression
    | atom #Atomic
    ;


atom : (number | variable | callfunction | orderfunctions)
    ;


number : NUM
    ;

assig_g : ID '<-' expr # Assig
    | ID '{' elements '}' #Assig
	| ID '[' expr ']' '<-' expr #AssigArray
    ;

variable: ID '[' expr ']' # ElementFromArray
    | ID # Var
	;

elements: (number | variable | callfunction) | (number | variable | callfunction) ',' elements
    ;

conditional : 'if' expr '{' body '}'
    | 'if' expr '{' body '}' 'else' '{' body '}'
    ;

orderfunctions: 'Map' NAME ID # MapFunction
    | 'Filter' NAME ID #FilterFunction
    ;


body_in : expr 
     | assig_g 
	 | conditional 
	 | loop 
	 | callfunction
     ;

body : body_in*
     ;


loop : 'while' expr '{' body '}'
    ;

function: NAME ID* '{' body '}'
    ;

callfunction: NAME expr*
    ;


ID : [a-z]+ ;
NAME: [A-Z][A-Za-z0-9]+ ;
NUM : [0-9]+ ; 
COMENT : '#'~[\n]*[\n]? -> skip ;
WS : [ \n]+ -> skip ;

