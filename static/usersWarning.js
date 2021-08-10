function readyToRemove() {

    let i = 0;
    let elements = document.querySelectorAll('input.readyP1');

    for (i; i < elements.length; i++) {
        if (elements[i].disabled === true) {
            (i === 1 ? alert("ADVERTENCIA: Una vez presione el botón para eliminar, toda la información del usuario se eliminará. Proceda con cuidado.") : false)
            elements[i].disabled = false;
            document.getElementById("botonreadyP1").innerHTML = "Volver a lo seguro. No estoy listo para eliminar.";
        } else {
            (i === 1 ? alert("Ha vuelto a lo seguro") : false)
            elements[i].disabled = true;
            document.getElementById("botonreadyP1").innerHTML = "¡Estoy listo para eliminar usuarios!";
        }
    }

}