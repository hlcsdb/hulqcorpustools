"use strict";

function testForm () {
    var textQuery = document.getElementById("text-query").value;
    var msgs = document.getElementsByClassName("msg");
    changeElements(msgs, textQuery);
}

async function changeElements (elementList, newText) {
    for (let i = 0; i < elementList.length; i++) {
        let pElement = elementList[i];
        let result = await changeElementText(newText);
        pElement.textContent = result;
    };
}

function changeElementText (newText) {

    const myPromise = new Promise(resolve => {
        setTimeout(() => {
            resolve(newText);
        }, 125);
    });
    return myPromise

}

const btn = document.getElementById("mess-up-btn");
btn.addEventListener("click", testForm);