# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request
from flask import make_response
from flask import redirect, url_for, flash, session
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = "Chave forte"

class NameForm(FlaskForm):
    name = StringField("Informe o seu nome", validators = [DataRequired()])
    sobrenome = StringField("Informe o seu sobrenome:", validators = [DataRequired()])
    instituicao = StringField("Informe a sua Insituição de ensino:", validators = [DataRequired()])
    disciplina = SelectField("Informe a sua disciplina:", choices = [('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de Projetos', 'Gestão de projetos')], validators = [DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário ou e-mail', validators = [DataRequired()], render_kw={"placeholder": "Usuário ou e-mail"})
    senha = PasswordField('Informe a sua senha', validators = [DataRequired()], render_kw={"placeholder": "Informe a sua senha"})
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    ip = request.remote_addr
    host = request.host
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['sobrenome'] = form.sobrenome.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data
        return redirect(url_for('index'))
    return render_template('index.html', form = form, nome = session.get('name'), sobrenome = session.get('sobrenome'), instituicao = session.get('instituicao'), disciplina = session.get('disciplina'), ip = ip, host = host, momento = datetime.utcnow())

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['usuario'] = form.usuario.data
        return redirect(url_for('loginResponse'))
    return render_template('login.html', form = form, momento = datetime.utcnow())

@app.route('/loginResponse')
def loginResponse():
    return render_template('loginResponse.html', usuario = session.get('usuario'), momento = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', nome=name)

@app.route('/user/')
def userr():
    return render_template('user.html')

@app.route('/rotainexistente')
def rotainexistente():
    return render_template('404.html')

@app.route('/user/<nome>/<prontuario>/<instituicao>')
def identificacao(nome, prontuario, instituicao):
    return render_template('user.html', nome=nome, prontuario=prontuario, instituicao=instituicao)

@app.route('/contextorequisicao/<nome>')
def contextorequisicao(nome):
    requisicao = request.headers.get('User-Agent')
    IP = request.remote_addr
    host = request.host
    return render_template('contextorequisicao.html', nome=nome, requisicao=requisicao, IP=IP, host=host)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    codigo = request.args['codigo']
    return f'<p>{codigo}</p>'

@app.route('/objetoresposta')
def objetoresposta():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br/')

from flask import abort
@app.route('/abortar')
def abortar():
    abort(404)
