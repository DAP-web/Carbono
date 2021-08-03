"use stritct";

function agregarCategoria() {

    if (document.getElementById("categoria").disabled) {
        document.getElementById("categoria").disabled = false;
        document.getElementById("agCat").innerHTML = "¡Click para agregar categoria!";
        document.getElementById("nuevaCategoria").disabled = true;
    } else {
        document.getElementById("categoria").disabled = true;
        document.getElementById("agCat").innerHTML = "¿Quieres seleccionar una categoria ya existente?";
        document.getElementById("nuevaCategoria").disabled = false;
    }


}
