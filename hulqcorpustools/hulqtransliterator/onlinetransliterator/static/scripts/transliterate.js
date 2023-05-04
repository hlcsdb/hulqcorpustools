"use strict";

async function getSourceText() {
    getSourceText.preventDefault();
    // const onSubmit = async (event) 
    var input_text = document.getElementById("input_text");
    console.log(input_text.value);

    var new_text = document.getElementById("new_text");
    new_text.textContent = input_text.value;
    // $("new_text")
    // new_text.textContent = 
    // var textQuery = document.getElementById("text-query").value;
    // var msgs = document.getElementsByClassName("msg");
}

var transliterateBtn = document.getElementById("transliterate-button")
transliterateBtn.addEventListener('submit', getSourceText)