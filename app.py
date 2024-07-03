from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from config_BD import connectionBD

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/temp'  # Carpeta donde se guardarán temporalmente las imágenes
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones de archivos permitidas

CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/usuariosgamers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la clave secreta
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

# Definición de tabla

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    pais = db.Column(db.String(50))
    imagen = db.Column(db.String(200))

    def __init__(self, nombre, apellido, nombre_usuario, correo, contraseña, sexo, pais=None, imagen=None):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contraseña = contraseña
        self.sexo = sexo
        self.pais = pais
        self.imagen = imagen

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"


with app.app_context():
    db.create_all()


@app.route("/")
def inicio():
    return render_template('registrarse.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/form', methods=['GET', 'POST'])
def registrarForm():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nombre_usuario = request.form['nombreUsuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        sexo = request.form['sexo']
        pais = request.form.get('pais')
        imagen = None
        
        # Manejo de la imagen de usuario
        if 'img-usuario' in request.files:
            file = request.files['img-usuario']
            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    imagen = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                else:
                    return jsonify({'message': 'Extensión de archivo no permitida'}), 400
        
        # Crear una instancia del modelo Usuario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombre_usuario,
            correo=correo,
            contraseña=contraseña,
            sexo=sexo,
            pais=pais,
            imagen=imagen
        )
        
        try:
            # Agregar el nuevo usuario a la sesión de SQLAlchemy
            db.session.add(nuevo_usuario)
            # Confirmar la transacción para que se guarde en la base de datos
            db.session.commit()
            
            # Si se ha cargado una imagen, actualizar la instancia de Usuario con la ruta de la imagen
            if imagen:
                nuevo_usuario.imagen = imagen
                db.session.commit()
            
            # Mensaje de éxito
            return redirect(url_for('inicio', msg='Usuario registrado con éxito'))
        
        except Exception as e:
            # Manejo de errores, por ejemplo, si falla la inserción en la base de datos
            db.session.rollback()
            # Puedes imprimir el error para depuración
            print(f"Error al registrar usuario: {str(e)}")
            # Redirigir al usuario de vuelta a la página de registro con mensaje de error
            return redirect(url_for('inicio')), 500
    return render_template('registrarse.html', msg='Método HTTP incorrecto')
    
@app.route('/iniciar-sesion', methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('iniciar-sesion.html')

    elif request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Verifica qué datos se están enviando desde el formulario
        print(f"Correo ingresado: {correo}, Contraseña ingresada: {contraseña}")

        # Busca el usuario en la base de datos usando SQLAlchemy
        usuario = Usuario.query.filter_by(correo=correo).first()

        # Verifica qué usuario se ha encontrado en la base de datos
        print(f"Usuario encontrado: {usuario}")

        # Comparación directa de contraseñas
        if usuario and usuario.contraseña == contraseña:
            session['logueado'] = True
            # session['id'] = usuario.id  # Opcional: si necesitas el ID del usuario en la sesión
            return render_template("admin.html")  # Redirige a la página de administrador
        else:
            # Usuario o contraseña incorrectas
            return render_template("cerrar.html", mensaje="Usuario o contraseña incorrectas")

    # Si el método HTTP no es GET ni POST, renderiza una página de error
    return render_template('cerrar.html')


@app.route('/admin')
def admin():
    if 'logueado' in session:
        return render_template("admin.html")
    else:
        return redirect(url_for("iniciar_sesion"))  # Redirige al inicio de sesión si no está logueado


if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
