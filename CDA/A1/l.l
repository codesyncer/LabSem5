%option yylineno
%{
    #define YYERROR_VERBOSE
    #include "y.tab.c"
%}
%%
if { 
    return IF; 
}
then {
    return THEN;
}
else {
    return ELSE;
}
endif {
    return ENDIF;
}
print {
    return PRINT;
}
newline {
    return NEWLINE;
}
\".*\" {
    strcpy(yylval.str, yytext+1);
    yylval.str[strlen(yytext)-2] = 0;
    return STRING;
}
\/\/.* {
    strcpy(yylval.str, yytext+2);
    return COMMENT;
}
[a-zA-Z][0-9a-zA-Z]* {
    strcpy(yylval.str, yytext+2);
    return ID;
}
[0-9]+ {
    yylval.num = atoi(yytext);
    return INT;
}
[\+\-\*\/=\<\>\(\);] { 
    return yytext[0];
}
=[=>] {
    strcpy(yylval.str, yytext);
    return OPERATOR;
}
[!<]= {
    strcpy(yylval.str, yytext);
    return OPERATOR;
}
[ \t\r\n]+ ;
. {
    printf("\n====\n");
    printf("Error at %d: lexical error, Unexpected symbol starting from '%c'", yylineno, *yytext);
    printf("\n====\n\n");
}
%%

int yywrap(){
    return 1;
}
void yyerror(const char* msg){
    printf("\n====\n");
    printf("Error at %d: %s", yylineno, msg);
    printf("\n====\n\n");
}
