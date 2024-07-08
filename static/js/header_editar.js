// document.addEventListener('DOMContentLoaded', function() {
//     const urls = {
//         tabla_usuarios: "{{ url_for('tabla_usuarios') }}",
//         ingresar_usuario: "{{ url_for('ingresar_usuario') }}"
//         // Agrega más URLs según sea necesario
//     };

    const headerContent = `
    <header id="header">
        <div>
            <img id="logo-header" src="../static/img/logo.jpg" alt="logo">
        </div>

        <p id="nombre-web">Ratón Gamer</p>
        <p id="app-admin">App Admin</p>

        <nav class="menu">
            <a class="hipervinc-header" href="${urls.tabla_usuarios}">Tabla usuarios</a>
            <a class="hipervinc-header" id="ingresarUsuarioLink" href="${urls.ingresar_usuario}">Ingresar Usuario</a>
        </nav>
    </header>
    `;

    // Agregar el contenido del encabezado al principio del body
    document.body.insertAdjacentHTML('afterbegin', headerContent);

    // Ruta del archivo CSS que deseas cargar dinámicamente
    const cssFile = '../static/css/estilos.css'; // Ajusta la ruta según tu estructura de archivos

    // Crear un elemento <link> para cargar el archivo CSS dinámicamente
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = cssFile;

    // Agregar el elemento <link> al <head> de tu documento
    document.head.appendChild(cssLink);

