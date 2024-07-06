

    function guardar() {
        let nombre_ingresado = document.getElementById("nombre").value; //input
        let apellido_ingresado = document.getElementById("apellido").value;
        let nombre_usuario_ingresado = document.getElementById("nombre_usuario").value;
        let correo_electronico_ingresado = document.getElementById("correo").value;
        let contraseña_ingresado = document.getElementById("contraseña").value;
        let sexo_ingresado = document.getElementById("sexo").value;
        let pais_ingresado = document.getElementById("pais").value;
        let imagen_ingresada = document.getElementById("imagen").files[0]; // Obtener el archivo de imagen seleccionado

        console.log(nombre_ingresado, apellido_ingresado, nombre_usuario_ingresado, correo_electronico_ingresado, contraseña_ingresado, sexo_ingresado, pais_ingresado, imagen_ingresada);

        // Crear un objeto FormData para enviar datos y archivos juntos
        let formData = new FormData();
        formData.append('nombre', nombre_ingresado);
        formData.append('apellido', apellido_ingresado);
        formData.append('nombre_usuario', nombre_usuario_ingresado);
        formData.append('correo_electronico', correo_electronico_ingresado);
        formData.append('contraseña', contraseña_ingresado);
        formData.append('sexo', sexo_ingresado);
        formData.append('pais', pais_ingresado);
        formData.append('imagen', imagen_ingresada);

        console.log(formData);

        let url = "http://localhost:5000/registro";
        var options = {
            body: formData, // Enviar formData en lugar de JSON.stringify(datos)
            method: 'POST',
            // No especificar 'Content-Type' aquí, el navegador lo manejará automáticamente para FormData
        };
        fetch(url, options)
            .then(function () {
                console.log("creado");
                alert("Grabado");
                // Redirecciona usando la URL dinámica definida
                window.location.href = urls.tabla_usuarios;  
            })
            .catch(err => {
                alert("Error al grabar");
                console.error(err);
            });
    }

    // Asigna la función guardar al evento click del botón
    document.getElementById('btnGuardar').addEventListener('click', guardar);

