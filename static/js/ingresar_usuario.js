function guardar() {
    let nombre_ingresado = document.getElementById("nombre").value //input
    let apellido_ingresado = document.getElementById("apellido").value 
    let nombre_usuario_ingresado = document.getElementById("nombre_usuario").value 
    let correo_electronico_ingresado = document.getElementById("correo_electronico").value 
    let contraseña_ingresado = document.getElementById("contraseña").value 
    let sexo_ingresado = document.getElementById("sexo").value 
    let pais_ingresado = document.getElementById("pais").value 
    let imagen_ingresada = document.getElementById("imagen").value 

    console.log(nombre_ingresado,apellido_ingresado,nombre_usuario_ingresado,correo_electronico_ingresado,contraseña_ingresado,sexo_ingresado,pais_ingresado,imagen_ingresada);
    // Se arma el objeto de js 
    let datos = {
        nombre: nombre_ingresado,
        apellido:apellido_ingresado,
        nombre_usuario:nombre_usuario_ingresado,
        correo_electronico:correo_electronico_ingresado,
        contraseña:contraseña_ingresado,
        sexo:sexo_ingresado,
        pais:pais_ingresado,
        imagen:imagen_ingresada
    }
    console.log(datos);
    
    let url = "http://localhost:5000/registro"
    var options = {
        body: JSON.stringify(datos),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
            // Devuelve el href (URL) de la página actual
            window.location.href = "../tabla_usuarios.html";  
            
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar" )
            console.error(err);
        })
}