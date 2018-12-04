%{
#include <stdio.h>
extern int yylex();
extern void yyerror(const char*);
char tokens[50][10];
int labels[50], label = 0;
int ttop = 0, ltop = -1, tmp_counter = 0;
FILE *code_file, *prod_file;

void push();
void pushs(char *yytext);
void cg_binary();
void cg_uminus();
void cg_assign();
void cg_eval();
void cg_after_if(int no_else);
void cg_after_else();
void cg_print();
void cg_string();
void cg_weval();
void cg_after_while();
void cg_before_while();
%}

%union { int con; int num; char str[50]; }

%token <con> WHILE
%token <con> ENDWHILE
%token <con> IF
%token <con> THEN
%token <con> ELSE
%token <con> ENDIF
%token <con> PRINT
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

%nonassoc IF1
%nonassoc ELSE
%left OPERATOR '<' '>'
%left '+' '-'
%left '*' '/'
%nonassoc UMINUS

%%
program: stmt_list { fprintf(prod_file,"%s\n", "program -> stmt_list"); };
stmt_list:
    stmt_list stmt { fprintf(prod_file,"%s\n", "stmt_list -> stmt_list stmt"); }
    | stmt { fprintf(prod_file,"%s\n", "stmt_list -> stmt"); };
stmt: assign_stmt { fprintf(prod_file,"%s\n", "stmt -> assign_stmt"); }
    | print_stmt { fprintf(prod_file,"%s\n", "stmt -> print_stmt"); }
    | if_stmt { fprintf(prod_file,"%s\n", "stmt -> if_stmt"); }
    | while_stmt { fprintf(prod_file,"%s\n", "stmt -> while_stmt"); };
assign_stmt: 
    ID {push();} '=' {push();} expr ';' { fprintf(prod_file,"%s\n", "assign_stmt -> ID = expr ;"); cg_assign(); }
    | error ';';
print_stmt:
    PRINT expr ';' { fprintf(prod_file,"%s\n", "print_stmt -> PRINT expr ;"); cg_print();}
    | PRINT STRING {push();} ';' { fprintf(prod_file,"%s\n", "print_stmt -> PRINT STRING ;"); cg_print();}
    | PRINT NEWLINE {push();} ';' { fprintf(prod_file,"%s\n", "print_stmt -> PRINT NEWLINE ;"); cg_print();}
    | PRINT error ';';
while_stmt:
    WHILE {cg_before_while();} expr {cg_weval();} THEN stmt_list ENDWHILE { fprintf(prod_file,"%s\n", "while_stmt -> while expr then stmt_list endwhile ;"); cg_after_while();}
if_stmt:
    top_if {cg_after_if(0);} ENDIF %prec IF1 { fprintf(prod_file,"%s\n", "if_stmt -> IF expr THEN stmt_list ENDIF"); } 
    | top_if {cg_after_if(1);} ELSE stmt_list ENDIF { fprintf(prod_file,"%s\n", "if_stmt -> IF expr THEN stmt_list ELSE stmt_list ENDIF"); cg_after_else(); }
    | error ENDIF;
top_if:
    IF expr {cg_eval();} THEN stmt_list
expr: '(' expr ')' { fprintf(prod_file,"%s\n", "expr -> ( expr )"); }
    | expr '+' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr + expr"); cg_binary();}
    | expr '-' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr - expr"); cg_binary();}
    | expr '*' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr * expr"); cg_binary();}
    | expr '/' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr / expr"); cg_binary();}
    | expr '<' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr < expr"); cg_binary();}
    | expr '>' {push();} expr { fprintf(prod_file,"%s\n", "expr -> expr > expr"); cg_binary();}
    | expr OPERATOR {push();} expr { fprintf(prod_file,"expr -> expr %s expr\n", $2); cg_binary();}
    | '-' expr %prec UMINUS { fprintf(prod_file,"%s\n", "expr -> - expr"); cg_uminus(); }
    | INT { fprintf(prod_file,"%s\n", "expr -> INT"); push(); }
    | ID { fprintf(prod_file,"%s\n", "expr -> ID"); push(); };   
%%
int main(){
    code_file = fopen("code", "w");
    prod_file = fopen("prod", "w");
    yyparse();
    fclose(prod_file);
    fclose(code_file);
    return 0;
}
void push()
{
    strcpy(tokens[++ttop], yytext);
}

void pushs(char *yytext){
    strcpy(tokens[++ttop], yytext);
}

void cg_binary()
{
    char tmp[10];
    sprintf(tmp, "tmp%d", tmp_counter++);
    fprintf(code_file, "OP(%s) %s %s %s\n", tokens[ttop-1], tmp, tokens[ttop-2], tokens[ttop]);
    ttop -= 2;
    strcpy(tokens[ttop], tmp);
}
void cg_uminus()
{
    char tmp[10];
    sprintf(tmp, "tmp%d", tmp_counter++);
    fprintf(code_file, "OP(-) %s 0 %s\n", tmp, tokens[ttop--]);
    strcpy(tokens[++ttop], tmp);
}
void cg_assign()
{ 
    fprintf(code_file, "MOV %s %s\n", tokens[ttop-2], tokens[ttop]);
    ttop -= 2;
}
void cg_eval()
{
 	fprintf(code_file, "TEST %s\n", tokens[ttop--]);
    fprintf(code_file, "JMP_ZERO L%d\n", ++label);
    labels[++ltop] = label;
}
void cg_after_if(int no_else)
{ 
	if(no_else) 
	{ 
        fprintf(code_file, "JMP L%d\nL%d:\n", ++label, labels[ltop--]);
        labels[++ltop] = label;
	}
	else
	{
    	fprintf(code_file, "L%d:\n", labels[ltop--]);
	}
}

void cg_after_else()
{ 
    fprintf(code_file, "L%d:\n", labels[ltop--]);
}

void cg_print()
{ 
    fprintf(code_file, "PRINT %s\n", tokens[ttop--]);
}
void cg_before_while(){
    fprintf(code_file, "L%d:\n", ++label);
    labels[++ltop] = label;
}
void cg_weval(){
    fprintf(code_file, "TEST %s\n", tokens[ttop--]);
    fprintf(code_file, "JMP_ZERO L%d\n", ++label);
    labels[++ltop] = label;
}

void cg_after_while(){
    fprintf(code_file, "JMP L%d\nL%d:\n", labels[ltop--], labels[ltop--]);
}