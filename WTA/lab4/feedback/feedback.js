function printForm() {
    let innerHtml, name, city, gender, comments;
    name = String(document.getElementsByTagName("form")[0].name.value);
    city = String(document.getElementsByTagName("form")[0].city.value);
    gender = String(document.getElementsByTagName("form")[0].gender.value);
    comments = String(document.getElementsByTagName("form")[0].comments.value);
    innerHtml = `<h2>By DOM</h2>Name: ${name}<br>City: ${city}<br>Gender: ${gender}<br>Comments: ${comments}`;
    document.getElementById("byDOM").innerHTML = innerHtml;

    name = String(document.getElementsByName("name")[0].value);
    city = String(document.getElementsByName("city")[0].value);
    gender = String(document.getElementsByName("gender")[0].value);
    comments = String(document.getElementsByName("comments")[0].value);
    innerHtml = `<h2>By Name</h2>Name: ${name}<br>City: ${city}<br>Gender: ${gender}<br>Comments: ${comments}`;
    document.getElementById("byName").innerHTML = innerHtml;

    name = String(document.getElementById("form_name").value);
    city = String(document.getElementById("form_city").value);
    gender = String(document.getElementById("form_gender").value);
    comments = String(document.getElementById("form_comments").value);
    innerHtml = `<h2>By Id</h2>Name: ${name}<br>City: ${city}<br>Gender: ${gender}<br>Comments: ${comments}`;
    document.getElementById("byId").innerHTML = innerHtml;
}