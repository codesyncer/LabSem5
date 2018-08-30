function printTotal() {
    let total = 0;
    let items = document.getElementsByClassName("items");
    for (let i = 0; i < items.length; ++i) {
        let price = Number(items[i].children[1].innerHTML);
        let quantity = Number(items[i].children[2].children[0].value);
        total += price*quantity;
    }
    document.getElementById("total").innerHTML = String(total);
}
function init(){
    let items = document.getElementsByClassName("items");
    for (let i = 0; i < items.length; ++i) {
        let inputobject = items[i].children[2].children[0];
        inputobject.onkeyup = inputobject.onchange = printTotal;
    }
    printTotal();
}