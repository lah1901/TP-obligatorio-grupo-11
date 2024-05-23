function testearDatos() {
    let correo = document.getElementById("correo").value.trim()
    let contraseña = document.getElementById("contraseña").value.trim()
    let error = document.getElementById("errores")

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
    
    else{
        alert("Formulario válido");
        return true;
    }

}