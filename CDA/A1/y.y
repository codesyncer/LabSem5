%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define N struct Node
int symbols[26];
extern int yylex();
extern void yyerror(char*);
int getVal(char symbol){
    return symbols[symbol-'a'];
}
int setVal(char symbol, int val){
    symbols[symbol-'a']= val;
    return val;
}
struct Node{
    char type;
    union {
        char id;
        int num;
        char contruct;
    }val;
    struct Node *left, *right;
};
N* newOpNode(int op, N* left, N* right){
    N *node= (N*)malloc(sizeof(N));
    node->left= left;
    node->right= right;
    node->type= 'o';
    node->val.contruct= op;
}
N* newcontructNode(char contruct, N* left, N* right){
    N *node= (N*)malloc(sizeof(N));
    node->left= left;
    node->right= right;
    node->type= 't';
    node->val.contruct= contruct;
}
N* newNumNode(int num){
    N *node= (N*)malloc(sizeof(N));
    node->left= NULL;
    node->right= NULL;
    node->type= 'n';
    node->val.num= num;
}
N* newIdNode(char id){
    N *node= (N*)malloc(sizeof(N));
    node->left= NULL;
    node->right= NULL;
    node->type= 'i';
    node->val.id= id;
}
int eval(N *);
void deleteTree(N *node){
    if(node == NULL) return;
    deleteTree(node->left);
    deleteTree(node->right);
    free(node);
}
void eop(N* node){
    printf("Ans: %d\n",eval(node));
    deleteTree(node);
    exit(0);
}
int eval(N* node){
    int den;
    if(node == NULL)
        return 0;
    if( node->type == 'n')
        return node->val.num;
    if( node->type == 'i')
        return getVal(node->val.id);
    if( node->type == 'o')
    switch(node->val.id){
        case '+':
            return eval(node->left) + eval(node->right);
        case '-':
            return eval(node->left) - eval(node->right);
        case '*':
            return eval(node->left) * eval(node->right);
        case '/':
            den = eval(node->right);
            if(den == 0)
                yyerror("Divide by Zero");
            return eval(node->left) / den;
        case '<':
            return eval(node->left) < eval(node->right);
        case '>':
            return eval(node->left) > eval(node->right);
        case '=':
            return setVal(node->left->val.id, eval(node->right));
        case ';':
            return eval(node->left), eval(node->right);
    }
    if(node->type == 't')
    switch(node->val.contruct){
        case 'i':
        if(eval(node->left)) eval(node->right->left);
        eval(node->right->right);
        break;
        case 'w':
        while(eval(node->left)) {
            eval(node->right);
        }
        break;
        case 'r':
        eop(node->left);
        break;
    }
    return 0;
}

%}

%union { struct Node *node; int num; char id; }
%start line
%token <num> number
%token <id> identifier
%token <id> basic_op
%token <node> RETURN
%token <node> IF
%token <node> WHILE
%type <node> term
%type <node> exp
%%
line :
    exp '\n' { eop($1); }
exp :
    term {$$ = $1;} |
    '[' basic_op exp exp ']'{ $$ = newOpNode($2, $3, $4); }|
    '[' RETURN exp ']'      { $$ = newcontructNode('r', $3, NULL); }|
    IF exp exp exp          { $$ = newcontructNode('i', $2, newcontructNode('x', $3, $4)); }|
    WHILE exp exp           { $$ = newcontructNode('w', $2, $3); };
term :
    number { $$ = newNumNode($1); }    |
    identifier { $$ = newIdNode($1); };
%%
int main(){
    memset(symbols, 0, 26*sizeof(int));
    yyparse();
    return 0;
}
/*
[; [= x 5] [; if [ < x 10 ] [= x [+ x 2]] [= x [* x 2]] [return x]]]
[; [= x 5] [; if [ < x 3 ] [= x [+ x 2]] [= x [* x 2]] [return x]]]
[; [= x 1] [; while [< x 9] [= x [+ x 2]] [return x] ]]
[; [; [= x 0] [= y 1]] [; while [< x 5] [;[= y [* y 2]] [= x [+ 1 x]]] [return y]]]
*/
