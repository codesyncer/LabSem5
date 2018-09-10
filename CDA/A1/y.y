%{
#include <stdio.h>
extern int yylex();
extern void yyerror(const char*);
%}

%union { int con; int num; char str[50]; }

%token <con> IF
%token <con> THEN
%token <con> ELSE
%token <con> ENDIF
%token <con> PRINT
%token <con> WHILE
%token <con> NEWLINE
%token <str> STRING
%token <str> COMMENT
%token <str> ID
%token <num> INT
%token <str> OPERATOR

%type <con> stmt_list
%type <con> stmt
%type <con> assign_stmt
%type <con> print_stmt
%type <con> if_stmt
%type <con> expr
%type <con> error

%%
program: stmt_list { printf("%s\n", "program -> stmt_list"); };
stmt_list:
    stmt_list stmt { printf("%s\n", "stmt_list -> stmt_list stmt"); }
    | stmt { printf("%s\n", "stmt_list -> stmt"); };
stmt: assign_stmt { printf("%s\n", "stmt -> assign_stmt"); }
    | print_stmt { printf("%s\n", "stmt -> print_stmt"); }
    | if_stmt { printf("%s\n", "stmt -> if_stmt"); };
assign_stmt: 
    ID '=' expr ';' { printf("%s\n", "assign_stmt -> ID = expr ;"); }
    | error ';';
print_stmt:
    PRINT expr ';' { printf("%s\n", "print_stmt -> PRINT expr ;"); }
    | PRINT STRING ';' { printf("%s\n", "print_stmt -> PRINT STRING ;"); }
    | PRINT NEWLINE ';' { printf("%s\n", "print_stmt -> PRINT NEWLINE ;"); }
    | error ';';
if_stmt:
    IF expr THEN stmt_list ENDIF { printf("%s\n", "if_stmt -> IF expr THEN stmt_list ENDIF"); } 
    | IF expr THEN stmt_list ELSE stmt_list ENDIF { printf("%s\n", "if_stmt -> IF expr THEN stmt_list ELSE stmt_list ENDIF"); }
    | error ENDIF;
expr: '(' expr ')' { printf("%s\n", "expr -> ( expr )"); }
    | expr '+' expr { printf("%s\n", "expr -> expr + expr"); }
    | expr '-' expr { printf("%s\n", "expr -> expr - expr"); }
    | expr '*' expr { printf("%s\n", "expr -> expr * expr"); }
    | expr '/' expr { printf("%s\n", "expr -> expr / expr"); }
    | expr '<' expr { printf("%s\n", "expr -> expr < expr"); }
    | expr '>' expr { printf("%s\n", "expr -> expr > expr"); }
    | '-' expr { printf("%s\n", "expr -> - expr"); }
    | INT { printf("%s\n", "expr -> INT"); }
    | ID { printf("%s\n", "expr -> ID"); };   
%%
int main(){
    yyparse();
    return 0;
}
