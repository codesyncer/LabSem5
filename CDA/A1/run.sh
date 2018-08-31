flex -o scan.c flexCode.l
if test $? -eq 0; then
    gcc -o scanner scan.c
    if test $? -eq 0; then
        ./scanner <<< $1
    fi
fi
