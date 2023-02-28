import datetime
from flask import Flask, render_template, redirect, request, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, DateField , SelectField
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user 

app = Flask (__name__) # create server
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']= 'Achu' #CONTRASENIA PARA LA DATABASE
db = SQLAlchemy(app) # Pasamos el servidor

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Modelos
class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Institucion(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    departamento = db.Column(db.String(10), nullable=False)
    ciudad = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Categorias(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Denuncia_Cat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    denuncia_id = db.Column(db.Integer, db.ForeignKey('denuncias.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    calificacion = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Denuncias(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    fecha = db.Column(db.String(80), nullable=False)
    institucion_id = db.Column(db.Integer, db.ForeignKey('institucion.id'))

#Formularios
class LoginForm(FlaskForm):
    email = EmailField('email')
    password= PasswordField()
    submit=SubmitField('Logueate!')

class RegisterForm(FlaskForm):
    name = StringField('name')
    email=EmailField('email')
    password=PasswordField('pass')
    submit=SubmitField('Registrate!')

class DenunciaForm(FlaskForm):
    fecha = DateField('fecha')
    institucion = StringField('institucion')
    saneamiento_descripcion = StringField('saneamiento_descripcion')
    saneamiento_calificacion = StringField('saneamiento_calificacion')
    agua_descripcion = StringField('agua_descripcion')
    agua_calificacion = StringField('agua_calificacion')
    internet_descripcion = StringField('internet_descripcion')
    internet_calificacion = StringField('internet_calificacion')
    infraestructura_descripcion = StringField('infraestructura_descripcion')
    infraestructura_calificacion = StringField('infraestructura_calificacion')
    mueblario_descripcion = StringField('mueblario_descripcion')
    mueblario_calificacion = StringField('mueblario_calificacion')
    cableado_descripcion = StringField('cableado_descripcion')
    cableado_calificacion = StringField('cableado_calificacion')

    calificacion = StringField('calificacion')
    descripcion = StringField('descripcion')

    submit = SubmitField('Enviar')

class InstitucionForm(FlaskForm):
    name = StringField('name')
    departamento = StringField('departamento')
    ciudad = StringField('ciudad')
    submit = SubmitField('Enviar')

#Crea la tablas, tiene que estar bajo las clases.
with app.app_context():
    db.create_all()

# Decorador
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=['POST','GET'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('institucion'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            print(current_user.id)
            return redirect(url_for('institucion'))
            #return 'me loguee'
        return "Invalid email or password!"
    
    return render_template('login.html', form=form)

@app.route('/institucion', methods=['POST','GET'])
def institucion():
    form = InstitucionForm()
    if form.validate_on_submit():
        new_institucion = Institucion(name=form.name.data, departamento=form.departamento.data, ciudad=form.ciudad.data, user_id=current_user.id)
        db.session.add(new_institucion)
        db.session.commit()
        return '<h1>se creo una institucion</h1>'
    return render_template('institucion.html', form=form)

@app.route('/denuncia', methods=['POST','GET'])
def denuncia():
    form = DenunciaForm()
    user = current_user.name
    # buscar en institucion el registro que tenga el user_id igual al current_user.id y constuir un objeto con ese registro
    inst = Institucion.query.filter_by(user_id=current_user.id).first()
    tipo_denuncia = Categorias.query.all()

    #generar un timestamp con el siguiente formato: 2020-12-31 23:59:59
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if form.validate_on_submit():
        new_denuncia = Denuncias(fecha=fecha, user_id=current_user.id, institucion_id=inst.id)
        db.session.add(new_denuncia)
        db.session.commit()

        registro = {
            'saneamiento': {
                'calificacion': form.saneamiento_calificacion.data,
                'descripcion': form.saneamiento_descripcion.data
            },
            'agua': {
                'calificacion': form.agua_calificacion.data,
                'descripcion': form.agua_descripcion.data
            },
            'internet': {
                'calificacion': form.internet_calificacion.data,
                'descripcion': form.internet_descripcion.data
            },
            'infraestructura': {
                'calificacion': form.infraestructura_calificacion.data,
                'descripcion': form.infraestructura_descripcion.data
            },
            "mueblario": {
                'calificacion': form.mueblario_calificacion.data,
                'descripcion': form.mueblario_descripcion.data
            },
            "cableado": {
                'calificacion': form.cableado_calificacion.data,
                'descripcion': form.cableado_descripcion.data
            }
        }

        for tipo in tipo_denuncia:
            new_denuncia_cat = Denuncia_Cat(denuncia_id=new_denuncia.id, categoria_id=tipo.id, calificacion=registro[tipo.name]['calificacion'], descripcion=registro[tipo.name]['descripcion'])
            db.session.add(new_denuncia_cat)
            db.session.commit()
        

        
        return '<h1>se creo una denuncia jeje</h1>'
    return render_template('denuncia.html', user=user, inst=inst ,form=form, fecha=fecha, tipo_denuncia=tipo_denuncia)

@app.route('/resumen/<int:denuncia_id>')
def resumen(denuncia_id):
    denuncia = Denuncias.query.filter_by(id=denuncia_id).first()
    denuncia_cat = Denuncia_Cat.query.filter_by(denuncia_id=denuncia_id).all()
    nombre = current_user.name
    fecha = denuncia.fecha
    institucion = Institucion.query.filter_by(id=denuncia.institucion_id).first()
    departamento = institucion.departamento
    ciudad = institucion.ciudad


    datos = {
        "nombre" : nombre,
        "fecha" : fecha,
        "institucion" : institucion.name,
        "departamento" : departamento,
        "ciudad" : ciudad,
        "categorias" : {}
    }



    print('------------------------------')
    print(f'nombre: {nombre}')
    print(f'fecha: {fecha}')
    print(f'institucion: {institucion.name}')
    print(f'departamento: {departamento}')
    print(f'ciudad: {ciudad}')
    print('------------------------------')
    for denuncia in denuncia_cat:
        categoria_name = Categorias.query.filter_by(id=denuncia.categoria_id).first()
        print(f'Categoria: {categoria_name.name}')
        print(f'Calificacion: {denuncia.calificacion}')
        print(f'Descripcion: {denuncia.descripcion}')
        print('------------------------------')
        datos["categorias"][categoria_name.name] = {
            "calificacion" : denuncia.calificacion,
            "descripcion" : denuncia.descripcion
        }

    print(datos)


    return render_template('resumen_denuncia.html', denuncia=denuncia, denuncia_cat=denuncia_cat , datos=datos)








# @app.route('/update/<int:todo_id>')
# @login_required
# def update_todo(todo_id):
#     todo_to_be_updated = Todo.query.filter_by(id=todo_id).first()
#     todo_to_be_updated.is_completed = not todo_to_be_updated.is_completed
#     db.session.commit()
#     return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(debug=True)