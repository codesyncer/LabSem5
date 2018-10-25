concert_ad{
    border: solid;
    margin: 20px;
    padding: 10px;
    line-height: 30px;
    display: block;
}
concert_ad > *{
    display: block;
}
concert_ad > name{
    color:blue;
    font-weight: bold;
    display: inline;
}
genre{
    color:maroon;
    font-style: italic;
}
place{
    float: right;
    color:blue;
}
performer{
    color:orange;
    display: inline;
    padding-right: 30px;
}
performer > role{
    display: none;
}
seller{
    font-weight: bold;
    color:black;
}
seller address{
    float: right;
}
ticket{
    padding-left: 30px;
    float: right;
}
ticket discount{
    display: none;
}
ticket[type="gold"]{
    color: goldenrod;
}
ticket[type="silver"]{
    color: silver;
}
ticket[type="ordinary"]{
    color: black;
}