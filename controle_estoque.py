import sqlite3
import datetime

DB_NAME = 'estoque.db'

# Conecta ao banco de dados
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Cria tabelas
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    perfil TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    quantidade INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    acao TEXT,
    data TEXT
)''')

conn.commit()

# Usuário admin padrão
try:
    cursor.execute('INSERT INTO usuarios (username, password, perfil) VALUES (?, ?, ?)', ('admin', 'admin123', 'admin'))
    conn.commit()
except sqlite3.IntegrityError:
    pass  # já existe

# Função de log
def registrar_log(usuario, acao):
    data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO logs (usuario, acao, data) VALUES (?, ?, ?)', (usuario, acao, data))
    conn.commit()

def login():
    username = input('Usuário: ')
    password = input('Senha: ')
    cursor.execute('SELECT perfil FROM usuarios WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    if result:
        print(f'Bem-vindo, {username}! Perfil: {result[0]}')
        registrar_log(username, 'Login realizado')
        return username, result[0]
    else:
        print('Usuário ou senha incorretos.')
        return None, None

def adicionar_produto(usuario):
    nome = input('Nome do produto: ')
    quantidade = int(input('Quantidade: '))
    cursor.execute('INSERT INTO produtos (nome, quantidade) VALUES (?, ?)', (nome, quantidade))
    conn.commit()
    print('Produto adicionado com sucesso.')
    registrar_log(usuario, f'Adicionou produto: {nome} ({quantidade})')

def visualizar_estoque():
    cursor.execute('SELECT id, nome, quantidade FROM produtos')
    produtos = cursor.fetchall()
    print('--- Estoque ---')
    for prod in produtos:
        print(f'ID: {prod[0]} | Nome: {prod[1]} | Quantidade: {prod[2]}')

def movimentar_estoque(usuario):
    produto_id = int(input('ID do produto: '))
    quantidade = int(input('Quantidade (use negativo para saída): '))
    cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
    result = cursor.fetchone()
    if result:
        nova_quantidade = result[0] + quantidade
        if nova_quantidade < 0:
            print('Erro: quantidade insuficiente.')
        else:
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
            conn.commit()
            print('Movimentação realizada.')
            registrar_log(usuario, f'Movimentou produto ID {produto_id} em {quantidade}')
    else:
        print('Produto não encontrado.')

def ver_logs():
    cursor.execute('SELECT usuario, acao, data FROM logs')
    logs = cursor.fetchall()
    print('--- LOGS ---')
    for log in logs:
        print(f'{log[2]} | {log[0]} | {log[1]}')

def main():
    usuario, perfil = login()
    if not usuario:
        return
    while True:
        print('\n1. Adicionar produto')
        print('2. Visualizar estoque')
        print('3. Movimentar estoque')
        if perfil == 'admin':
            print('4. Ver logs')
        print('0. Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            adicionar_produto(usuario)
        elif opcao == '2':
            visualizar_estoque()
        elif opcao == '3':
            movimentar_estoque(usuario)
        elif opcao == '4' and perfil == 'admin':
            ver_logs()
        elif opcao == '0':
            print('Saindo...')
            registrar_log(usuario, 'Logout')
            break
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    main()
