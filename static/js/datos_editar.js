// Procedimiento para traer los datos del registro a editar
// Ej: "id=9&nombre=bulbasaur"
let cadena = location.search; // Cadena con los símbolos & y =

// Crear un objeto URLSearchParams con la cadena
// El objeto URLSearchParams en JavaScript es una
// interfaz que proporciona métodos y propiedades para
// trabajar con las cadenas de consulta (query strings) en URLs.
// Facilitando la obtención de parámetros y valores individuales
let datos = new URLSearchParams(cadena);

// Crear un objeto para almacenar los nombres de las variables y sus valores
let resultado = {};

// Iterar sobre los parámetros y guardar los nombres y valores en el objeto resultado
for (const [nombre, valor] of datos) {
    resultado[nombre] = valor;
    resultado[apellido] = valor;
    resultado[nombre_usuario] = valor;
    resultado[correo] = valor;
    resultado[contraseña] = valor;
    resultado[sexo] = valor;
    resultado[pais] = valor;
    resultado[imagen] = valor
    resultado[rol]= valor

}

// Imprimir el resultado
// console.log(resultado); // Esto mostrará un objeto con las variables y sus valores


// Procedimiento para mostrar los datos a editar en el formulario de edición
document.getElementById("id").value = resultado["id"]
document.getElementById("nombre").value = resultado["nombre"]
document.getElementById("apellido").value = resultado["apellido"]
document.getElementById("nombre_usuario").value = resultado["nombre_usuario"]
document.getElementById("correo").value = resultado["correo"]
document.getElementById("contraseña").value = resultado["contraseña"]
document.getElementById("sexo").value = resultado["sexo"]
document.getElementById("pais").value = resultado["pais"]
document.getElementById("imagen").value = resultado["imagen"]
document.getElementById("rol").value = resultado["rol"]