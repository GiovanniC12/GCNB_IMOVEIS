import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('imoveis.db')
    c = conn.cursor()
    
    # Tabela de imóveis
    c.execute('''CREATE TABLE IF NOT EXISTS imoveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        preco REAL,
        localizacao TEXT,
        tipo TEXT,
        imagem TEXT
    )''')
    
    # Tabela de administradores
    c.execute('''CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    # Tabela de contatos
    c.execute('''CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        mensagem TEXT NOT NULL
    )''')
    
    # Adiciona um administrador padrão (senha: "admin123")
    try:
        c.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                  ("admin", generate_password_hash("admin123")))
    except sqlite3.IntegrityError:
        pass  # Admin já existe
    
    # Adiciona imóveis de exemplo
    c.execute("SELECT COUNT(*) FROM imoveis")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO imoveis (titulo, descricao, preco, localizacao, tipo, imagem) VALUES (?, ?, ?, ?, ?, ?)",
                      [
                          ("Casa 3 Quartos", "Casa ampla com jardim", 500000, "São Paulo", "Casa", "casa1.jpg"),
                          ("Apartamento Centro", "Ap. 2 quartos, vista para o mar", 350000, "Rio de Janeiro", "Apartamento", "ap1.jpg")
                      ])
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('imoveis.db')
    conn.row_factory = sqlite3.Row
    return conn