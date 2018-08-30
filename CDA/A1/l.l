%{
    #include "y.tab.h"
%}
%%
[ \t]               ;
return              { return RETURN; }
if                  { return IF; }
while               { return WHILE; }
[+-]?[1-9][0-9]*    { yylval.num= atoi(yytext); return number; }
0                   { yylval.num= 0; return number; }
[a-z]      	        { yylval.id=yytext[0]; return identifier; }
[\+\-\*\/=;\<\>]    { yylval.id=yytext[0]; return basic_op; }
[\[\]\n]            { return yytext[0];}
.                   { printf("Error: Unknown Symbol '%c'\n", *yytext); exit(0); }
%%

int yywrap(){ return 0; }
void yyerror(char* msg){ printf("Error: %s\n", msg); exit(0); }
