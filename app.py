from flask import Flask, render_template, redirect, request, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, DateField
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask (__name__) # create server
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']= 'Achu' #CONTRASENIA PARA LA DATABASE
db = SQLAlchemy(app) # Pasamos el servidor

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class LoginForm(FlaskForm):
    email = EmailField('email')
    password= PasswordField()
    submit=SubmitField('Logueate!')

#Registro
class RegisterForm(FlaskForm):
    name = StringField('name')
    email=EmailField('email')
    password=PasswordField('pass')
    submit=SubmitField('Registrate!')

#Cramos una tabla
class User (UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class InstitucionForm(FlaskForm):
    name = StringField('name')
    departamento = StringField('departamento')
    ciudad = StringField('ciudad')
    submit = SubmitField('Enviar')

class Institucion(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    departamento = db.Column(db.String(10), nullable=False)
    ciudad = db.Column(db.String(10), nullable=False)

class Saneamiento(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class InstalacionElectrica(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Agua(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Infraestructura(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Mueblario(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class Internet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))
    calificacion = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)

class DenunciaForm(FlaskForm):
    fecha = DateField('fecha')
    categoria = StringField('categoria')
    institucion = StringField('Institucion')
    submit = SubmitField('Enviar')

class Denuncias(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    fecha = db.Column(db.Date(), nullable=False)
    intitucion_id = db.Column(db.Integer, db.ForeignKey('Institucion.id'))

# class Category(FlaskForm()):
#     titulo = StringField('titulo')
#     calificacion = StringField('calificacion')
#     descripcion = StringField('descripcion')
#     submit = SubmitField('Enviar')

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     titulo = db.Column(db.String(80), nullable=False)
#     calificacion = db.Column(db.String(), nullable=False)
#     descripcion = db.Column(db.String(200), nullable=True)


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
        return '<h1>cree un usuario</h1>'
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            return redirect(url_for('todo'))
            #return 'me loguee'
        return "Invalid email or password!"
    
    return render_template('login.html', form=form)

@app.route('/formulario', methods=['POST','GET'])
def formulario():
    form = InstitucionForm()
    if form.validate_on_submit():
        new_institucion = Institucion(name=form.name.data, departamento=form.departamento.data, ciudad=form.ciudad.data)
        db.session.add(new_institucion)
        db.session.commit()
        return '<h1>se creo una institucion</h1>'
    return render_template('formulario.html', form=form)







# @app.route('/update/<int:todo_id>')
# @login_required
# def update_todo(todo_id):
#     todo_to_be_updated = Todo.query.filter_by(id=todo_id).first()
#     todo_to_be_updated.is_completed = not todo_to_be_updated.is_completed
#     db.session.commit()
#     return redirect(url_for('todo'))

if __name__ == '__main__':
    app.run(debug=1)