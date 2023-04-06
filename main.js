function showLogIn() {
    var formArea = document.querySelector("#formStuff");
    formArea.innerHTML = document.getElementById("temp-login").innerHTML;
    document.getElementById("options").style.display = 'none';
}

function showSignUp() {
    var formArea = document.querySelector("#formStuff");
    formArea.innerHTML = document.getElementById("temp-signup").innerHTML;
    document.getElementById("options").style.display = 'none';
}

function goBack() {
    document.querySelector("#formStuff").innerHTML = '';
    document.getElementById("options").style.display = 'block';
}