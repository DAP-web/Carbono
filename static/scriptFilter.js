function cambioDecision() {

    if (document.getElementById("updateBTN").style.display == "block") {
        document.getElementById("updateBTN").style.display = "none";
        document.getElementById("deleteBTN").style.display = "none";
        document.getElementById("filtersInputs").style.display = "block";
        document.getElementById("formUPD-FIL").action = "/filterTasks";
        document.getElementById("decisionboton").innerHTML = "No filtrar tareas";
    } else {
        document.getElementById("updateBTN").style.display = "block";
        document.getElementById("deleteBTN").style.display = "block";
        document.getElementById("filtersInputs").style.display = "none";
        document.getElementById("formUPD-FIL").action = "/checkTask";
        document.getElementById("decisionboton").innerHTML = "Filtrar tareas";
    }

}