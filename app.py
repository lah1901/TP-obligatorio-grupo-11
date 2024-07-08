from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__, template_folder='templates')
# Carpeta donde se guardarán temporalmente las imágenes
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/temp')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones de archivos permitidas
# Tamaño máximo del archivo subido (por ejemplo, 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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

    def __init__(self, nombre, apellido, nombre_usuario, correo, contraseña, sexo, pais=None, imagen=None, rol=1):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contraseña = contraseña
        self.sexo = sexo
        self.pais = pais
        self.imagen = imagen
        self.rol = rol
        
    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"

# Crear todas las tablas definidas en los modelos
with app.app_context():
    db.create_all()

# Definición de rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Guarda la ruta de la imagen en la base de datos, si es necesario
        return redirect(url_for('uploaded_file', filename=filename))

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
    if session.get('logueado'):
        return render_template('foro.html', usuario=usuarios)
    else:
        mensaje = 'Por favor inicia sesión para acceder al foro.'
        return render_template('iniciar-sesion.html', mensaje=mensaje)

@app.route('/tabla_usuarios')
def tabla_usuarios():
    usuarios = Usuario.query.all()

    return render_template('tabla_usuarios.html', usuarios=usuarios)

@app.route('/ingresar_usuario')
def ingresar_usuario():
    return render_template('ingresar_usuario.html')

# Función para verificar extensiones de archivos permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Retornar todos los registros en un Json
@app.route("/usuarios",  methods=['GET'])
def usuarios():
    # Consultar en la tabla todos los usuarios
    # all_registros -> lista de objetos
    all_registros = Usuario.query.all()

    # Lista de diccionarios
    data_serializada = []
    
    for objeto in all_registros:
        data_serializada.append({"id":objeto.id, "nombre":objeto.nombre, "apellido":objeto.apellido, "nombre_usuario":objeto.nombre_usuario, "correo":objeto.correo, "contraseña":objeto.contraseña, "sexo":objeto.sexo, "pais":objeto.pais, "imagen":objeto.imagen})

@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST', 'PUT'])
def editar_usuario(id):
    # Lógica para obtener y editar el usuario con el ID especificado
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST' :
        # or request.method == 'PUT'
        # Actualizar el usuario con los datos recibidos del formulario o JSON
        usuario.nombre = request.json.get('nombre', usuario.nombre)
        usuario.apellido = request.json.get('apellido', usuario.apellido)
        usuario.nombre_usuario = request.json.get('nombre_usuario', usuario.nombre_usuario)
        usuario.correo = request.json.get('correo', usuario.correo)
        usuario.contraseña = request.json.get('contraseña', usuario.contraseña)
        usuario.sexo = request.json.get('sexo', usuario.sexo)
        usuario.pais = request.json.get('pais', usuario.pais)
        usuario.imagen = request.json.get('imagen', usuario.imagen)
        usuario.rol = request.json.get('rol', usuario.rol)

        db.session.commit()
        
        # Redirigir a la página de tabla de usuarios o a donde sea necesario después de editar
        return redirect(url_for('tabla_usuarios'))

    # Renderizar el formulario de edición con los datos del usuario
    return render_template('editar_usuario.html', usuario=usuario)


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
        if usuario:
            if usuario.contraseña == contraseña:
                session['logueado'] = True
                # Verificar el rol del usuario y redirigir según el rol
                if usuario.rol == '2':
                    return render_template("usuarioRegistrado.html")
                elif usuario.rol == '1':
                    # Redirigir a la página de tabla de usuarios
                    return redirect(url_for('tabla_usuarios'))
                else:
                    return render_template("cerrar.html", mensaje="Rol de usuario no válido o indefinido")
            else:
                return render_template("cerrar.html", mensaje="Contraseña incorrecta")
        else:
            return render_template("cerrar.html", mensaje="Usuario no encontrado")


@app.route('/cerrar-sesion')
def cerrar_sesion():
    # Limpiar la sesión al cerrar sesión
    session.clear()
    return redirect(url_for('index'))

@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    
    # Se busca a la usuarios por id en la DB
    usuario = Usuario.query.get(id)

    # Se elimina de la DB
    db.session.delete(usuario)
    db.session.commit()

    data_serializada = [{"id":usuario.id, "nombre":usuario.nombre, "apellido":usuario.apellido, "nombre_usuario":usuario.nombre_usuario, "correo":usuario.correo, "contraseña":usuario.contraseña, "sexo":usuario.sexo, "pais":usuario.pais, "imagen":usuario.imagen}]

    return jsonify(data_serializada)

@app.route("/registro", methods=['POST']) 
def registro():
    try:
        data = request.get_json()  # Obtener los datos JSON del request

        # Validar que todos los campos necesarios están presentes
        required_fields = ['nombre', 'apellido', 'nombre_usuario', 'correo', 'contraseña', 'sexo', 'pais', 'imagen']
        for field in required_fields:
            if field not in data:
                return {"error": f"Missing field: {field}"}, 400

        # Crear un nuevo registro con los datos recibidos
        nuevo_registro = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            nombre_usuario=data['nombre_usuario'],
            correo=data['correo'],
            contraseña=data['contraseña'],
            sexo=data['sexo'],
            pais=data['pais'],
            imagen=data['imagen'],
            rol=data['rol']
        )

        # Añadir y confirmar el nuevo registro en la base de datos
        db.session.add(nuevo_registro)
        db.session.commit()

        return {"message": "Registro creado exitosamente", "usuario_id": nuevo_registro.id}, 201

    except Exception as e:
        # Manejo de cualquier error que pueda ocurrir
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
