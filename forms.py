from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar login')
    botao_submit_login = SubmitField('Fazer Login')


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")
    ])
    confirmacao_senha = PasswordField('Confirme a Senha', validators=[
        DataRequired(),
        EqualTo('senha', message='As senhas devem coincidir.')
    ])
    botao_submit_criarconta = SubmitField('Criar Conta')
