from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os

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

# Definición del modelo Usuario
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
    rol = db.Column(db.String(8), nullable=False, default='usuario')

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"

# Crear todas las tablas definidas en los modelos
with app.app_context():
    db.create_all()

# Definición de rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/trailers')
def trailers():
    return render_template('trailers.html')

@app.route('/reseñas')
def reseñas():
    return render_template('reseñas.html')

@app.route('/foro')
def foro():
    return render_template('foro.html')

@app.route('/tabla_usuarios.html')
def tabla_usuarios():
    # Lógica para obtener y renderizar la tabla de usuarios
    return render_template('tabla_usuarios.html')



@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        # Agrega aquí el resto de campos que deseas actualizar
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar_usuario.html', usuario=usuario)

# Ruta alternativa para edición de usuario, renombrada
@app.route('/editar_usuario_info/<int:id>', methods=['GET', 'POST'])
def editar_usuario_info(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        # Agrega aquí el resto de campos que deseas actualizar
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar_usuario.html', usuario=usuario)

# Función para verificar extensiones de archivos permitidas
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
            imagen=imagen,
            rol='2'  # Asignar rol por defecto
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
            
            # Redirigir al usuario a la página de inicio después de registrarse
            return redirect(url_for('index', msg='Usuario registrado con éxito'))
        
        except Exception as e:
            # Manejo de errores, por ejemplo, si falla la inserción en la base de datos
            db.session.rollback()
            print(f"Error al registrar usuario: {str(e)}")
            return redirect(url_for('index')), 500
    
    # Renderizar la página de registro por defecto si el método no es POST
    return render_template('registrarse.html', msg='Método HTTP incorrecto')
    
@app.route('/iniciar-sesion', methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('iniciar-sesion.html')

    elif request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        # Buscar el usuario en la base de datos usando SQLAlchemy
        usuario = Usuario.query.filter_by(correo=correo).first()

        # Comparación directa de contraseñas
        if usuario and usuario.contraseña == contraseña:
            session['logueado'] = True
            # Verificar el rol del usuario y redirigir según el rol
            if usuario.rol == '2':
                return render_template("usuarioRegistrado.html")
            elif usuario.rol == '1':
                usuarios = Usuario.query.all()
                return render_template("tabla_usuarios.html", usuarios=usuarios)
            else:
                return render_template("cerrar.html", mensaje="Rol de usuario no válido")
        else:
            return render_template("cerrar.html", mensaje="Usuario o contraseña incorrectas")

    # Si el método HTTP no es GET ni POST, renderiza una página de error
    return render_template('cerrar.html')

@app.route('/cerrar-sesion')
def cerrar_sesion():
    # Limpiar la sesión al cerrar sesión
    session.clear()
    return redirect(url_for('index'))
    # Modificar un registro

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if request.form.get('_method') == 'PUT':
        try:
            usuario.nombre = request.form.get('nombre', usuario.nombre)
            usuario.apellido = request.form.get('apellido', usuario.apellido)
            usuario.nombre_usuario = request.form.get('nombreUsuario', usuario.nombre_usuario)
            usuario.correo = request.form.get('correo', usuario.correo)
            usuario.contraseña = request.form.get('contraseña', usuario.contraseña)
            usuario.sexo = request.form.get('sexo', usuario.sexo)
            usuario.pais = request.form.get('pais', usuario.pais)
            usuario.imagen = request.form.get('img-usuario', usuario.imagen)

            db.session.commit()

            return jsonify({
                "mensaje": "Usuario actualizado correctamente",
                "id": usuario.id,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "nombre_usuario": usuario.nombre_usuario,
                "correo": usuario.correo,
                "contraseña": usuario.contraseña,
                "sexo": usuario.sexo,
                "pais": usuario.pais,
                "imagen": usuario.imagen
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {str(e)}")
            return jsonify({"error": "Error al actualizar usuario"}), 500

    return jsonify({"error": "Método no permitido"}), 405


@app.route('/borrar/<int:id>', methods=['DELETE'])
def borrar(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({
        "message": "Usuario eliminado correctamente",
        "id": usuario.id
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
