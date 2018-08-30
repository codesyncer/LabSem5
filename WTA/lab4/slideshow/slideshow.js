var imgs = [
    'http://library.nitk.ac.in/images/NITK1.jpg',
    'https://qph.fs.quoracdn.net/main-qimg-8762fa7aa9790f1861b0b864cfb391f0-c',
    'http://www.mangaloretoday.com/contentfiles/2017/aug/NITK%20%2030%20nov%2017.jpg',
];
var index = 0;
function slide_start(){
    document.getElementById('img_main').src = imgs[index];
}
function slide_dir(dir){
    index = (index+dir+imgs.length)%imgs.length;
    document.getElementById('img_main').src = imgs[index];
}