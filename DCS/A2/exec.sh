n=`expr $1 - 1`
for i in `seq 0 $n`;
do
    gnome-terminal -- python3 main.py $1 $i
done