"use strict";

var monthsArr, userGlobal = "", emailGlobal = "", dateGlobal = "", rolGlobal = "";

monthsArr = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];

//Funcion que ensenha el titulo del mes y anho que se escoja
function selectMonth() {
    let strDate = "", dateArr = [], strMonth = "";

    strDate = document.getElementById("inputDate").value;
    dateArr = strDate.split("/");
    strMonth = monthsArr[parseInt(dateArr[0]) - 1];
    strDate = strMonth.concat("/", dateArr[1], "/", dateArr[2]);
    document.getElementById("boxMesIterativo").style.display = "block";
    document.getElementById("addElement").style.display = "block";
    document.getElementById("mesIterativo").innerHTML = strDate;
    dateGlobal = strDate;

    cleanListToDo();
    cleanValues("inputDate");

    if (rolGlobal === "admin") {
        listUsersTask()
    }
}

//Limpia la caja del input
function cleanValues(pID) {
    document.getElementById(pID).value = "";
}

function cleanListToDo() {
    let list, listLength = 0, i = 0;

    list = document.getElementById("lista");
    listLength = list.childNodes.length;

    while (i < listLength) {
        list.removeChild(list.childNodes[0]);
        i++;
    }
}


//Navbar to the right START***********************
// Function expression to select elements `

const selectElement = (s) => document.querySelector(s);
const navLinks = document.querySelectorAll(".nav-link");

selectElement(".burger-menu-icon").addEventListener("click", () => {
    selectElement(".nav-list").classList.toggle("active");
    selectElement(".burger-menu-icon").classList.toggle("toggle")

    navLinks.forEach((link, index) => {
        if (link.style.animation) {
            link.style.animation = ""
        } else {
            link.style.animation = `navLinkAnimate 0.5s ease forwards ${index / 7 + 0.5}s`
            console.log(index / 7 + 0.5)
        }
    })
});

navLinks.forEach(link => {
    link.addEventListener("click", () => {
        selectElement(".nav-list").classList.toggle("active");
        selectElement(".burger-menu-icon").classList.toggle("toggle");

        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = ""
            } else {
                link.style.animation = `navLinkAnimate 0.5s ease forwards ${index / 7 + 0.5}s`
                console.log(index / 7 + 0.5)
            }
        })
    })
})

//Navbar to the right END*************************