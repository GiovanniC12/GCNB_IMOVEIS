from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from database import get_db
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Substitua por uma chave segura
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Configuração de e-mail
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "seu_email@gmail.com",  # Substitua pelo seu e-mail
    "sender_password": "sua_senha_de_app",  # Use uma senha de aplicativo do Gmail
    "recipient_email": "destinatario@exemplo.com"  # E-mail que recebe os contatos
}

# Classe de usuário para Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM admin WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['username'])
    return None

@app.route('/')
def index():
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    localizacao = request.args.get('localizacao', '')
    tipo = request.args.get('tipo', '')

    query = "SELECT * FROM imoveis WHERE 1=1"
    params = []
    if preco_min:
        query += " AND preco >= ?"
        params.append(preco_min)
    if preco_max:
        query += " AND preco <= ?"
        params.append(preco_max)
    if localizacao:
        query += " AND localizacao LIKE ?"
        params.append(f'%{localizacao}%')
    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    imoveis = c.fetchall()
    conn.close()
    return render_template('index.html', imoveis=imoveis)

@app.route('/imovel/<int:id>')
def imovel(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM imoveis WHERE id = ?", (id,))
    imovel = c.fetchone()
    conn.close()
    if imovel:
        return render_template('imovel.html', imovel=imovel)
    return redirect(url_for('index'))

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        
        msg = MIMEText(f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}")
        msg['Subject'] = 'Contato - Imobiliária XYZ'
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        
        try:
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.send_message(msg)
            server.quit()
            flash('Mensagem enviada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao enviar mensagem: {str(e)}', 'danger')
        
        return redirect(url_for('contato'))
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'])
            login_user(user_obj)
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            preco = float(request.form['preco'])
            localizacao = request.form['localizacao']
            tipo = request.form['tipo']
            imagem = request.form['imagem']
            c.execute("INSERT INTO imoveis (titulo, descricao, preco, localizacao, tipo, imagem) VALUES (?, ?, ?, ?, ?, ?)",
                      (titulo, descricao, preco, localizacao, tipo, imagem))
        elif action == 'update':
            id = int(request.form['id'])
            titulo = request.form['titulo']
            descricao = request.form['descricao']
            preco = float(request.form['preco'])
            localizacao = request.form['localizacao']
            tipo = request.form['tipo']
            imagem = request.form['imagem']
            c.execute("UPDATE imoveis SET titulo = ?, descricao = ?, preco = ?, localizacao = ?, tipo = ?, imagem = ? WHERE id = ?",
                      (titulo, descricao, preco, localizacao, tipo, imagem, id))
        elif action == 'delete':
            id = int(request.form['id'])
            c.execute("DELETE FROM imoveis WHERE id = ?", (id,))
        conn.commit()
    
    c.execute("SELECT * FROM imoveis")
    imoveis = c.fetchall()
    conn.close()
    return render_template('admin.html', imoveis=imoveis)

if __name__ == '__main__':
    app.run(debug=True, port=5000)