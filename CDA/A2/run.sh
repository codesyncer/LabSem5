yacc y.y
flex l.l
if test $? -eq 0; then
    gcc lex.yy.c
    if test $? -eq 0; then
        echo -e '\n\n======\nOUTPUT\n======\n\n'
        ./a.out < $1
    fi
fi
echo -e "\n"