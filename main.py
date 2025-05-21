from flask import Flask, render_template, url_for, request, redirect, flash
from forms import FormLogin, FormCriarConta
from flask_sqlalchemy import SQLAlchemy
from extensoes import db
from model.Usuario import Usuario
from model.UsuarioAuth import UsuarioAuth
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.config['DEBUG'] = False

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave-padrao-segura')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#importar do render


# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'luizpaulolpf1991@gmail.com'
app.config['MAIL_PASSWORD'] = '123'
app.config['MAIL_DEFAULT_SENDER'] = 'luizpaulolpf1991@gmail.com'
mail = Mail(app)

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Nome da função da rota de login

@login_manager.user_loader
def load_user(user_id):
    return UsuarioAuth.query.get(int(user_id))

# Rota de contato
@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        msg = Message("Nova mensagem do site", recipients=['seuemail@gmail.com'])
        msg.body = f"""
        Nome: {nome}
        Email: {email}
        Mensagem:
        {mensagem}
        """
        try:
            mail.send(msg)
            flash("Mensagem enviada com sucesso!", 'alert-success')
        except Exception as e:
            flash("Erro ao enviar mensagem. Tente novamente.", 'alert-danger')
            print("Erro ao enviar e-mail:", e)

        return redirect(url_for("contato"))
    return render_template("contato.html")

# Página principal
@app.route('/')
def home():
    return render_template('home.html')

# Rota de login e criação de conta
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    # LOGIN
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = UsuarioAuth.query.filter_by(email=form_login.email.data).first()
        if usuario:
            if usuario.verificar_senha(form_login.senha.data):
                login_user(usuario, remember=form_login.lembrar_dados.data)
                flash('Login realizado com sucesso!', 'alert-success')
                return redirect(url_for('usuarios'))
            else:
                flash('E-mail ou senha incorretos.', 'alert-danger')
        else:
            flash('Usuário não encontrado ou não autorizado.', 'alert-warning')

    # CRIAR CONTA
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        usuario_existente = UsuarioAuth.query.filter_by(email=form_criarconta.email.data).first()
        if usuario_existente:
            flash('E-mail já cadastrado. Faça login ou use outro e-mail.', 'alert-warning')
        else:
            novo_usuario = UsuarioAuth(
                username=form_criarconta.username.data,
                email=form_criarconta.email.data
            )
            novo_usuario.set_senha(form_criarconta.senha.data)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login.', 'alert-success')
            return redirect(url_for('login'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'alert-info')
    return redirect(url_for('home'))

# Página de usuários
@app.route('/usuarios', methods=['GET', 'POST'])
@login_required
def usuarios():
    if request.method == 'POST':
        novo_usuario = Usuario(
            name=request.form['name'],
            address=request.form['address'],
            postcode=request.form['postcode'],
            city=request.form['city'],
            contact=request.form['contact'],
            cargo=request.form['cargo'],
            email=request.form['email'],
            others=request.form['others'],
            website=request.form['website']
        )
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('usuarios'))

    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista_usuarios)

# Editar usuário
@app.route('/usuarios/edit/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def edit_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == 'POST':
        usuario.name = request.form['name']
        usuario.address = request.form['address']
        usuario.postcode = request.form['postcode']
        usuario.city = request.form['city']
        usuario.contact = request.form['contact']
        usuario.cargo = request.form['cargo']
        usuario.email = request.form['email']
        usuario.website = request.form['website']
        usuario.others = request.form['others']

        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'alert-success')
        return redirect(url_for('usuarios'))

    return render_template('edit_usuario.html', usuario=usuario)

# Deletar usuário
@app.route('/usuarios/delete/<int:usuario_id>', methods=['POST'])
@login_required
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado com sucesso!', 'alert-danger')
    return redirect(url_for('usuarios'))

@app.route('/criar_tabelas')
def criar_tabelas():
    try:
        db.create_all()
        return "Tabelas criadas com sucesso no banco remoto!"
    except Exception as e:
        return f"Erro ao criar tabelas: {e}"


# Rodar o app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
