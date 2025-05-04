
import sqlite3
import datetime
import tkinter as tk
from tkinter import messagebox

DB_NAME = 'estoque.db'

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect(DB_NAME)
    return conn, conn.cursor()

# Função de log
def registrar_log(cursor, usuario, acao):
    data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO logs (usuario, acao, data) VALUES (?, ?, ?)", (usuario, acao, data))
    cursor.connection.commit()

# Criação das tabelas no banco de dados
def criar_tabelas(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, perfil TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, quantidade INTEGER)")
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, acao TEXT, data TEXT)")

# Função de login
def login(cursor, window_login, entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Login", "Por favor, preencha ambos os campos.")
        return

    cursor.execute("SELECT perfil FROM usuarios WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()

    if result:
        perfil = result[0]
        messagebox.showinfo("Login", f"Bem-vindo, {username}! Perfil: {perfil}")
        registrar_log(cursor, username, 'Login realizado')
        window_login.destroy()
        abrir_ventana_principal(cursor, username, perfil)
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")

# Tela de Login
def tela_login(cursor):
    window_login = tk.Tk()
    window_login.title("Login - Controle de Estoque")

    tk.Label(window_login, text="Usuário:").pack(pady=5)
    entry_username = tk.Entry(window_login)
    entry_username.pack(pady=5)

    tk.Label(window_login, text="Senha:").pack(pady=5)
    entry_password = tk.Entry(window_login, show="*")
    entry_password.pack(pady=5)

    tk.Button(window_login, text="Entrar", command=lambda: login(cursor, window_login, entry_username, entry_password)).pack(pady=10)

    window_login.mainloop()

# Funções da tela principal
def abrir_ventana_principal(cursor, usuario, perfil):
    window_main = tk.Tk()
    window_main.title("Sistema de Controle de Estoque")

    def adicionar_produto():
        nome = entry_nome_produto.get()
        quantidade = entry_quantidade_produto.get()

        if not nome or not quantidade.isdigit():
            messagebox.showerror("Adicionar Produto", "Por favor, preencha todos os campos corretamente.")
            return

        quantidade = int(quantidade)
        cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        cursor.connection.commit()
        registrar_log(cursor, usuario, f'Adicionou produto: {nome} ({quantidade})')
        messagebox.showinfo("Adicionar Produto", "Produto adicionado com sucesso!")

    def visualizar_estoque():
        cursor.execute("SELECT id, nome, quantidade FROM produtos")
        produtos = cursor.fetchall()
        estoque_listbox.delete(0, tk.END)
        for prod in produtos:
            estoque_listbox.insert(tk.END, f'ID: {prod[0]} | Nome: {prod[1]} | Quantidade: {prod[2]}')

    def movimentar_estoque():
        produto_id = entry_id_produto.get()
        quantidade = entry_quantidade_movimento.get()

        if not produto_id.isdigit() or not quantidade.isdigit():
            messagebox.showerror("Movimentação", "Por favor, preencha todos os campos corretamente.")
            return

        produto_id = int(produto_id)
        quantidade = int(quantidade)

        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        result = cursor.fetchone()

        if result:
            nova_quantidade = result[0] + quantidade
            if nova_quantidade < 0:
                messagebox.showerror("Movimentação", "Erro: Quantidade insuficiente.")
            else:
                cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))
                cursor.connection.commit()
                registrar_log(cursor, usuario, f'Movimentou produto ID {produto_id} em {quantidade}')
                messagebox.showinfo("Movimentação", "Movimentação realizada com sucesso!")
        else:
            messagebox.showerror("Movimentação", "Produto não encontrado.")

    def ver_logs():
        cursor.execute("SELECT usuario, acao, data FROM logs")
        logs = cursor.fetchall()
        logs_text.delete(1.0, tk.END)
        for log in logs:
            logs_text.insert(tk.END, f'{log[2]} | {log[0]} | {log[1]}\n')

    tk.Label(window_main, text="Produto Nome:").pack(pady=5)
    entry_nome_produto = tk.Entry(window_main)
    entry_nome_produto.pack(pady=5)

    tk.Label(window_main, text="Quantidade:").pack(pady=5)
    entry_quantidade_produto = tk.Entry(window_main)
    entry_quantidade_produto.pack(pady=5)

    tk.Button(window_main, text="Adicionar Produto", command=adicionar_produto).pack(pady=10)
    tk.Button(window_main, text="Visualizar Estoque", command=visualizar_estoque).pack(pady=10)

    tk.Label(window_main, text="ID do Produto para movimentação:").pack(pady=5)
    entry_id_produto = tk.Entry(window_main)
    entry_id_produto.pack(pady=5)

    tk.Label(window_main, text="Quantidade (negativa para saída):").pack(pady=5)
    entry_quantidade_movimento = tk.Entry(window_main)
    entry_quantidade_movimento.pack(pady=5)

    tk.Button(window_main, text="Movimentar Estoque", command=movimentar_estoque).pack(pady=10)

    if perfil == 'admin':
        tk.Button(window_main, text="Ver Logs", command=ver_logs).pack(pady=10)

    tk.Button(window_main, text="Sair", command=window_main.quit).pack(pady=10)

    estoque_listbox = tk.Listbox(window_main, width=50, height=10)
    estoque_listbox.pack(pady=10)

    if perfil == 'admin':
        logs_text = tk.Text(window_main, height=10, width=50)
        logs_text.pack(pady=10)

    window_main.mainloop()

# Função principal para rodar o programa
def main():
    conn, cursor = conectar_banco()
    criar_tabelas(cursor)

    try:
        cursor.execute("INSERT INTO usuarios (username, password, perfil) VALUES (?, ?, ?)", ('admin', 'admin123', 'admin'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    tela_login(cursor)
    conn.close()

if __name__ == "__main__":
    main()
