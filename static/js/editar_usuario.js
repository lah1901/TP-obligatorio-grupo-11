// document.addEventListener('DOMContentLoaded', function() {
//     const urls = {
//         tabla_usuarios: "../tabla_usuarios.html",
//         ingresar_usuario: "../templates/ingresar_usuario.html"
//         // Agrega más URLs según sea necesario
//     };

    function modificar() {
        let id = document.getElementById("id").value; // Obtener el ID del usuario a modificar
        let nombre_ingresado = document.getElementById("nombre").value;
        let apellido_ingresado = document.getElementById("apellido").value;
        let nombre_usuario_ingresado = document.getElementById("nombre_usuario").value;
        let correo_electronico_ingresado = document.getElementById("correo_electronico").value;
        let contraseña_ingresado = document.getElementById("contraseña").value;
        let sexo_ingresado = document.querySelector('input[name="sexo"]:checked').value; // Obtener el valor del radio button seleccionado
        let pais_ingresado = document.getElementById("pais").value;
        let imagen_ingresada = document.getElementById("imagen").value; // Asegúrate de que estás manejando la imagen adecuadamente, normalmente se usa un input type="file"

        // Crear el objeto con los datos del formulario
        let datos = {
            nombre: nombre_ingresado,
            apellido: apellido_ingresado,
            nombre_usuario: nombre_usuario_ingresado,
            correo_electronico: correo_electronico_ingresado,
            contraseña: contraseña_ingresado,
            sexo: sexo_ingresado,
            pais: pais_ingresado,
            imagen: imagen_ingresada
        };

        console.log(datos);

        // URL para la solicitud PUT (asegúrate de que la ruta y el puerto coincidan con tu backend Flask)
        let url = `http://localhost:5000/update/${id}`;

        // Opciones para la solicitud Fetch
        let options = {
            body: JSON.stringify(datos), // Convertir datos a formato JSON
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        // Realizar la solicitud Fetch
        fetch(url, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al modificar el registro');
                }
                console.log("Modificado correctamente");
                alert("Registro modificado exitosamente");
                window.location.href = urls.tabla_usuarios; // Redirigir a la página de tabla de usuarios después de modificar
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Error al modificar el registro");
            });
    }

    // Asigna la función modificar al evento click del botón
    document.getElementById('btnModificar').addEventListener('click', modificar);

