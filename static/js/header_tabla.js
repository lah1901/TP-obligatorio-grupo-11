document.addEventListener('DOMContentLoaded', function() {
    const headerContent = `
    <header id="header">
        <div>
            <img id="logo-header" src="static/img/logo.jpg" alt="logo">
        </div>

        <p id="nombre-web">Ratón Gamer</p>
        <p id="app-admin">App Admin</p>

        <nav class="menu">
            <a id="ingresarUsuarioLink" href="#">Ingresar Usuario</a>
        </nav>
    </header>
    `;

    // Agregar el contenido del encabezado al principio del body
    document.body.insertAdjacentHTML('afterbegin', headerContent);

    // Manipula los enlaces después de que la página se haya cargado completamente
    const ingresarUsuarioLink = document.getElementById('ingresarUsuarioLink');
    ingresarUsuarioLink.href = urls.ingresar_usuario;
    // Puedes manipular otros enlaces aquí según sea necesario
});
