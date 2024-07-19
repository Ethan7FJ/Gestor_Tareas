from flask import *
import mysql.connector
from werkzeug.security import *
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
import math

app = Flask(__name__)

app.config['SECRET_KEY'] = '1235451'

dab = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gestor"
)

curso = dab.cursor()

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'johanrfetecua@gmail.com'
app.config['MAIL_PASSWORD'] = 'tteq pdkx odyr avca'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ('Johan Fetecua :D', 'johanrfetecua@gmail.com')
mail = Mail(app)

@app.route('/')
def iniciar():
    return render_template('index.html')

@app.route('/grafica_usu')
def grafica_usu():

    curso = dab.cursor()

    usu = session.get('usuario_u')
    curso.execute('SELECT id_u FROM usuarios WHERE usuario_u = %s',(usu,))
    id_usu = curso.fetchone()[0]

    buscarT1 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Por asignar' AND id_u = %s"
    curso.execute(buscarT1,(id_usu,))
    datosT1 = curso.fetchone()[0]

    buscarT2 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Terminado' AND id_u = %s"
    curso.execute(buscarT2,(id_usu,))
    datosT2 = curso.fetchone()[0]

    buscarT3 = "SELECT COUNT(*) FROM tareas WHERE estado = 'En proceso' AND id_u = %s"
    curso.execute(buscarT3,(id_usu,))
    datosT3 = curso.fetchone()[0]

    x = [datosT1,datosT2,datosT3]
    y = ["T.por asignar","T.Terminado","T.En proceso"]


    plt.bar(y,x)
    plt.xlabel('Categora')
    plt.ylabel('Cantidades')
    plt.grid()
    plt.show()

    return render_template('PrincipalUsu.html')

@app.route('/grafica_admin')
def grafica_admin():

    curso = dab.cursor()

    buscar = "SELECT COUNT(*) FROM usuarios"
    curso.execute(buscar)
    datos = curso.fetchone()[0]

    buscarT1 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Por asignar'"
    curso.execute(buscarT1)
    datosT1 = curso.fetchone()[0]

    buscarT2 = "SELECT COUNT(*) FROM tareas WHERE estado = 'Terminado'"
    curso.execute(buscarT2)
    datosT2 = curso.fetchone()[0]

    buscarT3 = "SELECT COUNT(*) FROM tareas WHERE estado = 'En proceso'"
    curso.execute(buscarT3)
    datosT3 = curso.fetchone()[0]

    x = [datos,datosT1,datosT2,datosT3]
    y = ["Usuarios","T.por asignar","T.Terminado","T.En proceso"]


    plt.bar(y,x)
    plt.xlabel('Categora')
    plt.ylabel('Cantidades')
    plt.grid()
    plt.show()

    return render_template('Principal.html')


@app.route('/token_expirado')
def token_expirado():
    return render_template('token_expirado.html')

#Inicio de sesion
@app.route('/', methods=['GET','POST'])
def iniciar():
    #Verificacion de crednciales de ingreso de acuerdo la rol
    usuario_u = request.form.get('usuario_u')
    contrasena_u = request.form.get('contrasena_u')

    curso = dab.cursor(dictionary=True)
    buscar = "SELECT usuario_u,contrasena_u,rol_u FROM usuarios WHERE usuario_u = %s"
    curso.execute(buscar,(usuario_u,))
    datos = curso.fetchone()
    
    if(datos and check_password_hash(datos['contrasena_u'],contrasena_u)):
        ##Crear sesion
        session['usuario_u'] = datos['usuario_u']
        session['rol_u'] = datos['rol_u']

        if datos['rol_u'] == 'Admin':
            return render_template('Principal.html')
        else:
            return render_template('PrincipalUsu.html')
    else:
        print("Sus credenciales son incorrectas")
        return render_template('index.html')


@app.route('/restablecer_contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    if request.method == 'POST':
        nueva_contra = request.form['passw']
        confirmar_contra = request.form['confir_passw']

        if nueva_contra != confirmar_contra:
            return "Las contraseñas no coinciden"

        passwordNuevo = generate_password_hash(nueva_contra)

        try:
            email = serializer.loads(token, salt='Restablecimiento de Contraseña', max_age=3600)  # Token válido por 1 hora
        except BadSignature:
            return redirect(url_for('token_expirado'))

        curso = dab.cursor()
        consulta = "UPDATE usuarios SET contrasena_u = %s WHERE email_u = %s"
        curso.execute(consulta, (passwordNuevo, email))
        dab.commit()
        return redirect(url_for('iniciar'))

    return render_template('restablecer_contrasena.html', token=token)

def enviar_em(email):
    token = serializer.dumps(email, salt='Restablecimiento de Contraseña')
    enlace = url_for('restablecer_contrasena', token=token, _external=True)
    mensaje = Message(
        subject='Restablecimiento de contraseña',
        recipients=[email],
        body=f'Para restablecer su contraseña, haz click en el enlace de abajo:\n{enlace}'
    )

    try:
        mail.send(mensaje)
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error enviando el correo: {e}")

@app.route('/recuperar_contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        enviar_em(email)
        return redirect(url_for('iniciar'))

    return render_template('recuperarPS.html')

@app.route('/regresar-usu-principal', methods=['GET','POST'])
def regresar_usu():
    
    return render_template('PrincipalUsu.html')

@app.route('/buscar_usuario_t',methods=['GET','POST'])
def buscar_tarea_usuario():

    busquedaUsuario = request.form.get('busquedaUsuario')

    curso = dab.cursor(dictionary=True)
    consultarTareas = 'SELECT * FROM tareas WHERE id_t = %s OR nombre_t LIKE %s'
    curso.execute(consultarTareas,(busquedaUsuario, "%" + busquedaUsuario + "%"))
    tareasUsuario = curso.fetchall()

    return render_template('resultadoBusUsuario.html',tareasUsuario=tareasUsuario, busquedaUsuario=busquedaUsuario)

@app.route('/buscar_tarea',methods=['GET','POST'])
def buscar_tarea():

    busqueda = request.form.get('busqueda')

    curso = dab.cursor(dictionary=True)
    consultar = 'SELECT * FROM tareas WHERE id_t = %s OR nombre_t LIKE %s'
    curso.execute(consultar,(busqueda, "%" + busqueda + "%"))
    tareas = curso.fetchall()

    return render_template('resultadoBus.html',tareas=tareas, busqueda=busqueda)

@app.route('/buscar_usuario',methods=['GET','POST'])
def buscar_usuario():

    busquedaU = request.form.get('busquedaU')

    curso = dab.cursor(dictionary=True)
    consultarU = 'SELECT * FROM usuarios WHERE id_u = %s OR nombre_u LIKE %s'
    curso.execute(consultarU,(busquedaU, "%" + busquedaU + "%"))
    UsuariosU = curso.fetchall()

    return render_template('resultadoBusUsu.html',UsuariosU=UsuariosU, busquedaU=busquedaU)

@app.route('/eliminar-tarea-usuario/<int:id>',methods=['GET','POST'])
def eliminar_tare_usu(id):

    curso = dab.cursor()
    curso.execute('DELETE FROM tareas WHERE id_t = %s',(id,))
    dab.commit()

    return redirect(url_for('tareas_usu'))

@app.route('/actualizar-tareas-usuario/<int:id>',methods=['GET','POST'])
def actu_tareas_usu(id):
        if request.method == 'POST':
            nombre_t = request.form.get('nombre_t')
            fecha_inicio_t = request.form.get('fecha_inicio_t')
            fecha_final_t = request.form.get('fecha_final_t')
            estado = request.form.get('estado')

            curso = dab.cursor()
            sql = "UPDATE tareas SET nombre_t = %s, fecha_inicio_t = %s, fecha_final_t = %s, estado = %s WHERE id_t =%s"
            curso.execute(sql,(nombre_t,fecha_inicio_t,fecha_final_t,estado,id))
            dab.commit()
            return render_template('PrincipalUsu.html')
        else:
            curso = dab.cursor()
            curso.execute('SELECT * FROM tareas WHERE id_t = %s',(id,))
            aid = curso.fetchall()
            curso.close()
            return render_template('modalTare_usu.html', tareas=aid[0])

@app.route('/actualizar-tareas/<int:id>',methods=['GET','POST'])
def actu_tareas(id):
        if request.method == 'POST':
            nombre_t = request.form.get('nombre_t')
            fecha_inicio_t = request.form.get('fecha_inicio_t')
            fecha_final_t = request.form.get('fecha_final_t')
            estado = request.form.get('estado')

            curso = dab.cursor()
            sql = "UPDATE tareas SET nombre_t = %s, fecha_inicio_t = %s, fecha_final_t = %s, estado = %s WHERE id_t =%s"
            curso.execute(sql,(nombre_t,fecha_inicio_t,fecha_final_t,estado,id))
            dab.commit()
            return render_template('Principal.html')
        else:
            curso = dab.cursor()
            curso.execute('SELECT * FROM tareas WHERE id_t = %s',(id,))
            aid = curso.fetchall()
            curso.close()
            return render_template('modalTare.html', tareas=aid[0])

@app.route('/actualizar-usuario/<int:id>',methods=['GET','POST'])
def actu_usuario(id):
        if request.method == 'POST':
            nombre_u = request.form.get('nombre_u')
            apellido_u = request.form.get('apellido_u')
            email_u = request.form.get('email_u')
            usuario_u = request.form.get('usuario_u')
            rol_u = request.form.get('rol_u')
            curso = dab.cursor()

            sql = "UPDATE usuarios SET nombre_u = %s, apellido_u = %s, email_u =%s, usuario_u = %s, rol_u = %s WHERE id_u = %s"
            curso.execute(sql,(nombre_u,apellido_u,email_u,usuario_u,rol_u,id))
            dab.commit()
            return render_template('Principal.html')
        else:
            curso = dab.cursor()
            curso.execute('SELECT * FROM usuarios WHERE id_u = %s',(id,))
            aid = curso.fetchall()
            curso.close()
            return render_template('modalUsu.html', lista=aid[0])

@app.route('/eliminar-tarea/<int:id>',methods=['GET','POST'])
def eliminar_tare(id):

    curso = dab.cursor()
    curso.execute('DELETE FROM tareas WHERE id_t = %s',(id,))
    dab.commit()

    return redirect(url_for('tareas'))

@app.route('/eliminar-usuario/<int:id>',methods=['GET','POST'])
def eliminar_usu(id):

    curso = dab.cursor()
    curso.execute('DELETE FROM tareas WHERE id_u = %s',(id,))
    curso.execute('DELETE FROM usuarios WHERE id_u = %s',(id,))
    dab.commit()

    return redirect(url_for('lista'))

@app.route('/regresar-usu', methods=['GET','POST'])
def regresar():
    session.pop('usuario_u',None)
    return redirect(url_for('iniciar'))

@app.route('/tareas-usu', methods=['GET','POST'])
def tareas_usu():
    usux = session.get('usuario_u')
    curso.execute('SELECT id_u FROM usuarios WHERE usuario_u = %s',(usux,))
    id_usu = curso.fetchone()[0]

    curso.execute('SELECT * FROM tareas WHERE id_u = %s',(id_usu,))
    listaT = curso.fetchall()
    return render_template('PrincipalUsu.html',listaT = listaT)

@app.route('/tareas', methods=['GET','POST'])
def tareas():
    curso = dab.cursor()
    curso.execute('SELECT * FROM tareas')
    listaT = curso.fetchall()
    return render_template('Principal.html',listaT = listaT)


@app.route('/lista', methods=['GET','POST'])
def lista():
    curso = dab.cursor()
    curso.execute('SELECT * FROM usuarios')
    lista = curso.fetchall()
    return render_template('Principal.html',lista = lista)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache,no-store-must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0

    return response


@app.route('/salir')
def salir():
    session.pop('usuario_u',None)
    return redirect(url_for('iniciar'))

@app.route('/Registro-Usuario-admin', methods=['GET','POST'])
def Usureg_admin():
    if request.method == 'POST':
        nombre_u = request.form.get('nombre_u')
        apellido_u = request.form.get('apellido_u')
        email_u = request.form.get('email_u')
        usuario_u = request.form.get('usuario_u')
        contrasena_u = request.form.get('contrasena_u')
        rol_u = request.form.get('rol_u')
        encripContra = generate_password_hash(contrasena_u)

        #Validar si el usuario ya existe

        curso = dab.cursor()
        curso.execute('SELECT * FROM usuarios WHERE usuario_u= %s OR email_u = %s',(usuario_u,email_u))
        existente = curso.fetchone()

        if existente:
            print("El usuario ya esta registra, intenta de nuevo")
            return render_template('registroUsuAdmin.html')

        else:
            curso.execute('INSERT INTO usuarios(nombre_u,apellido_u,email_u,usuario_u,contrasena_u,rol_u) VALUE(%s,%s,%s,%s,%s,%s)',(nombre_u,apellido_u,email_u,usuario_u,encripContra,rol_u))
            dab.commit()
            print("El usuario ha sido registrado exitosamente")
            return render_template('Principal.html')

    return render_template('registroUsuAdmin.html')


#Registrar usuario
@app.route('/Registro-Usuario', methods=['GET','POST'])
def Usureg():
    if request.method == 'POST':
        nombre_u = request.form.get('nombre_u')
        apellido_u = request.form.get('apellido_u')
        email_u = request.form.get('email_u')
        usuario_u = request.form.get('usuario_u')
        contrasena_u = request.form.get('contrasena_u')
        rol_u = request.form.get('rol_u')
        encripContra = generate_password_hash(contrasena_u)

        #Validar si el usuario ya existe

        curso = dab.cursor()
        curso.execute('SELECT * FROM usuarios WHERE usuario_u= %s OR email_u = %s',(usuario_u,email_u))
        existente = curso.fetchone()

        if existente:
            print("El usuario ya esta registra, intenta de nuevo")
            return render_template('registroUsu.html')

        else:
            curso.execute('INSERT INTO usuarios(nombre_u,apellido_u,email_u,usuario_u,contrasena_u,rol_u) VALUE(%s,%s,%s,%s,%s,%s)',(nombre_u,apellido_u,email_u,usuario_u,encripContra,rol_u))
            dab.commit()
            print("El usuario ha sido registrado exitosamente")
            return redirect(url_for('iniciar'))

    return render_template('registroUsu.html')


#Regitrar tarea
@app.route('/Registro-Tareas-admin', methods=['GET','POST'])
def Registrar_admin():
    if request.method == 'POST':
        
        nombre_t = request.form.get('nombre_t')
        fecha_inicio_t = request.form.get('fecha_inicio_t')
        fecha_final_t = request.form.get('fecha_final_t')
        estado = request.form.get('estado')

        curso = dab.cursor()
        #verificacion de que la tarea no este registrado
        curso.execute('SELECT * FROM tareas WHERE nombre_t = %s',(nombre_t,))
        existe = curso.fetchone()

        if existe:
            print("La tarea ya esta registrada")
            return render_template('registroTarAdmin.html')
        
        else:
            #insertar los datos ingresados a la tabla tareas
            curso.execute('INSERT INTO tareas(nombre_t,fecha_inicio_t,fecha_final_t,estado) VALUE(%s,%s,%s,%s)',(nombre_t,fecha_inicio_t,fecha_final_t,estado))
            dab.commit()
            print("La tarea ha sido registrada")
            return render_template('Principal.html')
        
    return render_template('registroTarAdmin.html')

@app.route('/Registro-Tareas', methods=['GET','POST'])
def Registrar():
    if request.method == 'POST':
        
        nombre_t = request.form.get('nombre_t')
        fecha_inicio_t = request.form.get('fecha_inicio_t')
        fecha_final_t = request.form.get('fecha_final_t')
        estado = request.form.get('estado')

        curso = dab.cursor()
        #verificacion de que la tarea no este registrado
        curso.execute('SELECT * FROM tareas WHERE nombre_t = %s',(nombre_t,))
        existe = curso.fetchone()

        if existe:
            print("La tarea ya esta registrada")
            return render_template('registroTar.html')
        
        else:
            usu = session.get('usuario_u')
            curso.execute('SELECT id_u FROM usuarios WHERE usuario_u = %s',(usu,))
            id_usu = curso.fetchone()[0]
            #insertar los datos ingresados a la tabla tareas
            curso.execute('INSERT INTO tareas(nombre_t,fecha_inicio_t,fecha_final_t,estado,id_u) VALUE(%s,%s,%s,%s,%s)',(nombre_t,fecha_inicio_t,fecha_final_t,estado,id_usu))
            dab.commit()
            print("La tarea ha sido registrada")
            return render_template('PrincipalUsu.html')
        
    return render_template('registroTar.html')

if __name__ == '__main__':
    app.run(debug=True)
    app.add_url_rule('/',view_func=iniciar)



