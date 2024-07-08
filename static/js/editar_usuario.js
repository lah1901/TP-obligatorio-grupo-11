function modificar() {
    let id = document.getElementById("id").value;
    let nombre_ingresado = document.getElementById("nombre").value;
    let apellido_ingresado = document.getElementById("apellido").value; 
    let nombre_usuario_ingresado = document.getElementById("nombre_usuario").value; 
    let correo_electronico_ingresado = document.getElementById("correo").value; 
    let contraseña_ingresado = document.getElementById("contraseña").value; 
    let sexo_ingresado = document.getElementById("sexo").value; 
    let pais_ingresado = document.getElementById("pais").value; 
    let imagen_ingresada = document.getElementById("imagen").value; 
    let rol = document.getElementById("rol").value;

    let datos = {
        nombre: nombre_ingresado,
        apellido: apellido_ingresado,
        nombre_usuario: nombre_usuario_ingresado,
        correo: correo_electronico_ingresado,
        contraseña: contraseña_ingresado,
        sexo: sexo_ingresado,
        pais: pais_ingresado,
        imagen: imagen_ingresada,
        rol: rol
    };

    console.log(datos);

    let url = "http://localhost:5000/update/"+id
    var options = {
        body: JSON.stringify(datos),
        method: 'PUT',
        
        headers: { 'Content-Type': 'application/json' },
        // el navegador seguirá automáticamente las redirecciones y
        // devolverá el recurso final al que se ha redirigido.
        redirect: 'follow'
    }
    fetch(url, options)
        .then(function () {
            console.log("modificado")
            alert("Registro modificado")

            //Puedes utilizar window.location.href para obtener la URL actual, redirigir a otras páginas
           window.location.href = "../tabla_usuarios.html";
          
        })
        .catch(err => {
            this.error = true
            console.error(err);
            alert("Error al Modificar")
        })      
}
