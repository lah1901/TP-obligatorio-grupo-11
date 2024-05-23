function testearDatos() {

    let nombre = document.getElementById("nombre").value.trim()
    let apellido = document.getElementById("apellido").value.trim()
    let nombreUsuario = document.getElementById("nombreUsuario").value.trim()
    let correo = document.getElementById("correo").value.trim()
    let contraseña = document.getElementById("contraseña").value.trim()
    let imgUsuario = document.getElementById("img-usuario").value.trim()
    let error = document.getElementById("errores")

    if (nombreUsuario === "") {
        error.textContent = "Introduzca su nombre de usuario.";
        error.style.color = "red";
        return false;
    }

    if (!/^[a-zA-Z]+$/.test(nombre)) {
        error.textContent = "Ingrese un nombre válido.";
        error.style.color = "red";
        return false;
    }

    if (!/^[a-zA-Z]+$/.test(apellido)) {
        error.textContent = "Ingrese un apellido válido.";
        error.style.color = "red";
        return false;
    }

    if (!/^[a-zA-Z]+$/.test(nombreUsuario)) {
        error.textContent = "Ingrese un nombre de usuario válido.";
        error.style.color = "red";
        return false;
    }

    if(!/^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/gm.test(correo)){
        error.textContent="Ingrese un correo válido.";
        error.style.color="red";
        return false;
    }

    if(!/^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{7,})\S$/.test(contraseña)){
        error.textContent="Contraseña: mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número.";
        error.style.color="red";
        return false;
    } 

    if(!/\.(jpg|jpeg|png|gif)$/i.test(imgUsuario)){
        error.textContent="Extensiones permitidas:.jpg,.jpeg,.png,.gif";
        error.style.color="red;"
        return false;
    } 
    
    else{
        alert("Formulario válido");
        return true;
    }
}
