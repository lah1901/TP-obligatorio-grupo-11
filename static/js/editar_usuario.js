function modificar() {
    let id = document.getElementById("id").value;
    let nombre_ingresado = document.getElementById("nombre").value;
    let apellido_ingresado = document.getElementById("apellido").value;
    let nombre_usuario_ingresado = document.getElementById("nombre_usuario").value;
    let correo_ingresado = document.getElementById("correo").value;
    let contraseña_ingresado = document.getElementById("contraseña").value;
    let sexo_ingresado = document.querySelector('input[name="sexo"]:checked').value;
    let pais_ingresado = document.getElementById("pais").value;
    let imagen_ingresada = document.getElementById("imagen").value;
    let rol_ingresado = document.getElementById("rol").value;

    let datos = {
        nombre: nombre_ingresado,
        apellido: apellido_ingresado,
        nombre_usuario: nombre_usuario_ingresado,
        correo: correo_ingresado,
        contraseña: contraseña_ingresado,
        sexo: sexo_ingresado,
        pais: pais_ingresado,
        imagen: imagen_ingresada,
        rol: rol_ingresado
    };

    console.log(datos);

    let url = `http://localhost:5000/editar_usuario/${id}`;
    var options = {
        body: JSON.stringify(datos),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
    };

    fetch(url, options)
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Error al modificar el registro');
        }
        return response.json();
    })
    .then(function(data) {
        console.log("modificado");
        alert("Registro modificado");
        window.location.href = urls.tabla_usuarios;
    })
    .catch(function(err) {
        console.error(err);
        alert("Error al Modificar");
    });
}