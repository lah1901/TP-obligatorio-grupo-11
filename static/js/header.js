// header.js

document.addEventListener('DOMContentLoaded', function() {
    // Definir el contenido del encabezado dinámico usando las URLs generadas por Flask
    const headerContent = `
    <nav class="menu">
        <a href="${urls.tabla_usuarios}">Tabla usuarios</a>
        <a href="${urls.ingresar_usuario}">Registrar usuario</a>
        <p>¡Hola!</p>
    </nav>
    `;

    // Actualizar el contenido del elemento con ID 'header' usando innerHTML
    document.getElementById("header").innerHTML = headerContent;
});
