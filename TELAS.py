import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def conectar():
    return sqlite3.connect('escola.db')

def cadastro_aluno():
    def salvar():
        nome = entry_nome.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        senha = entry_senha.get()
        if nome and email and senha:
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Aluno (nome, email, endereco, telefone, senha) VALUES (?, ?, ?, ?, ?)",
                    (nome, email, endereco, telefone, senha)
                )
                conn.commit()
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Email já cadastrado.")
            conn.close()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")

    win = tk.Toplevel()
    win.title("Cadastro de Aluno")
    win.geometry("600x400")

    tk.Label(win, text="Nome").pack(pady=5)
    entry_nome = tk.Entry(win)
    entry_nome.pack(pady=5)
    tk.Label(win, text="Email").pack(pady=5)
    entry_email = tk.Entry(win)
    entry_email.pack(pady=5)
    tk.Label(win, text="Endereço").pack(pady=5)
    entry_endereco = tk.Entry(win)
    entry_endereco.pack(pady=5)
    tk.Label(win, text="Número de Telefone").pack(pady=5)
    entry_telefone = tk.Entry(win)
    entry_telefone.pack(pady=5)
    tk.Label(win, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(win, show="*")
    entry_senha.pack(pady=5)
    tk.Button(win, text="Cadastrar", command=salvar).pack(pady=10)

def cadastro_professor():
    def salvar():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        proficiencia = entry_prof.get()
        if nome and email and senha and proficiencia:
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO Professor (nome, proficiencia, email, endereco, telefone, senha, id_escola) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (nome, proficiencia, email, endereco, telefone, senha, 1)
                )
                conn.commit()
                messagebox.showinfo("Sucesso", "Professor cadastrado!")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Email já cadastrado.")
            conn.close()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    win = tk.Toplevel()
    win.title("Cadastro de Professor")
    win.geometry("600x400")

    tk.Label(win, text="Nome").pack(pady=5)
    entry_nome = tk.Entry(win)
    entry_nome.pack(pady=5)
    tk.Label(win, text="Proficiência").pack(pady=5)
    entry_prof = tk.Entry(win)
    entry_prof.pack(pady=5)
    tk.Label(win, text="Email").pack(pady=5)
    entry_email = tk.Entry(win)
    entry_email.pack(pady=5)
    tk.Label(win, text="Endereço").pack(pady=5)
    entry_endereco = tk.Entry(win)
    entry_endereco.pack(pady=5)
    tk.Label(win, text="Número de Telefone").pack(pady=5)
    entry_telefone = tk.Entry(win)
    entry_telefone.pack(pady=5)
    tk.Label(win, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(win, show="*")
    entry_senha.pack(pady=5)
    
    tk.Button(win, text="Cadastrar", command=salvar).pack(pady=10)

def carregar_professores(tree, escola_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_professor, nome, email FROM Professor WHERE id_escola=?", (escola_id,))
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()

def carregar_alunos(tree):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_aluno, nome, email FROM Aluno")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()
    
def carregar_turmas(tree,escola_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Turma.id_turma, Turma.nome, Turma.descricao, Turma.especialidade,
               Professor.nome, Escola.nome
        FROM Turma
        JOIN Professor ON Turma.id_professor = Professor.id_professor
        JOIN Escola ON Turma.id_escola = Escola.id_escola
        WHERE Escola.id_escola = ?
    """, (escola_id,))
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()

def cadastro_escola():
    def salvar():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        endereco = entry_endereco.get()
        telefone = entry_telefone.get()
        if nome and email and senha:
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Escola (nome, email, senha, endereco, telefone, descricao) VALUES (?, ?, ?, ?, ?, ?)",
                               (nome, email, senha, endereco, telefone, ""))
                conn.commit()
                messagebox.showinfo("Sucesso", "Escola cadastrada com sucesso!")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Email já cadastrado.")
            conn.close()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    win = tk.Toplevel()
    win.title("Cadastro de Escola")
    win.geometry("600x400")

    tk.Label(win, text="Nome da Instituição").pack(pady=5)
    entry_nome = tk.Entry(win)
    entry_nome.pack(pady=5)
    tk.Label(win, text="Endereço").pack(pady=5)
    entry_endereco = tk.Entry(win)
    entry_endereco.pack(pady=5)
    tk.Label(win, text="Telefone").pack(pady=5)
    entry_telefone = tk.Entry(win)
    entry_telefone.pack(pady=5)
    tk.Label(win, text="Email").pack(pady=5)
    entry_email = tk.Entry(win)
    entry_email.pack(pady=5)
    tk.Label(win, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(win, show="*")
    entry_senha.pack(pady=5)
    tk.Button(win, text="Cadastrar", command=salvar).pack(pady=10)

def tela_cadastro():
    win = tk.Toplevel()
    win.title("Escolha o tipo de cadastro")
    win.geometry("600x400")

    tk.Label(win, text="Tipo de cadastro").pack(pady=10)
    tk.Button(win, text="Aluno", command=cadastro_aluno, width=20).pack(pady=5)
    tk.Button(win, text="Professor", command=cadastro_professor, width=20).pack(pady=5)
    tk.Button(win, text="Escola", command=cadastro_escola, width=20).pack(pady=5)

def tela_login():
    def verificar():
        email = entry_email.get()
        senha = entry_senha.get()
        if email and senha:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Escola WHERE email=? AND senha=?", (email, senha))
            escola = cursor.fetchone()
            cursor.execute("SELECT * FROM Professor WHERE email=? AND senha=?", (email, senha))
            prof = cursor.fetchone()
            cursor.execute("SELECT * FROM Aluno WHERE email=? AND senha=?", (email, senha))
            aluno = cursor.fetchone()
            if escola:
                messagebox.showinfo("Login", "Login de Escola bem-sucedido!")
                win.destroy()
                interface_administracao(escola[0]) 
            elif prof:
                messagebox.showinfo("Login", "Login de Professor bem-sucedido!")
                win.destroy()
                # Aqui futuramente pode chamar ambiente_professor(prof[0])
            elif aluno:
                messagebox.showinfo("Login", "Login de Aluno bem-sucedido!")
                win.destroy()
                ambiente_aluno(aluno[0])
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")
            conn.close()

    win = tk.Toplevel()
    win.title("Login")
    win.geometry("600x400")

    tk.Label(win, text="Email").pack(pady=10)
    entry_email = tk.Entry(win)
    entry_email.pack(pady=5)
    tk.Label(win, text="Senha").pack(pady=10)
    entry_senha = tk.Entry(win, show="*")
    entry_senha.pack(pady=5)
    tk.Button(win, text="Entrar", command=verificar).pack(pady=15)

def interface_administracao(escola_id):
    win = tk.Toplevel()
    win.title("Painel Administrativo da Escola")
    win.geometry("700x500")

    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill='both')

    frame_professores = ttk.Frame(notebook)
    frame_alunos = ttk.Frame(notebook)
    frame_turmas = ttk.Frame(notebook)

    notebook.add(frame_professores, text="Professores")
    notebook.add(frame_alunos, text="Alunos")
    notebook.add(frame_turmas, text="Turmas")
    
    tk.Label(frame_professores, text="Lista de Professores", font=("Arial", 12)).pack(pady=5)
    tree_prof = ttk.Treeview(frame_professores, columns=("ID", "Nome", "Email"), show='headings')
    for col in ("ID", "Nome", "Email"):
        tree_prof.heading(col, text=col)
    tree_prof.pack(expand=True, fill='both')
    carregar_professores(tree_prof, escola_id)

    
    tk.Label(frame_alunos, text="Lista de Alunos", font=("Arial", 12)).pack(pady=5)
    tree_alunos = ttk.Treeview(frame_alunos, columns=("ID", "Nome", "Email"), show='headings')
    for col in ("ID", "Nome", "Email"):
        tree_alunos.heading(col, text=col)
    tree_alunos.pack(expand=True, fill='both')
    carregar_alunos(tree_alunos)

    tk.Label(frame_turmas, text="Lista de Turmas", font=("Arial", 12)).pack(pady=5)
    tree_turmas = ttk.Treeview(frame_turmas, columns=("ID", "Nome", "Descrição","Especialidade", "Professor", "Escola" ), show='headings')
    for col in ("ID", "Nome", "Descrição","Especialidade", "Professor", "Escola" ):
        tree_turmas.heading(col, text=col)
    tree_turmas.pack(expand=True, fill='both')
    carregar_turmas(tree_turmas,escola_id)

def ambiente_aluno(id_aluno):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome FROM Aluno WHERE id_aluno = ?", (id_aluno,))
    resultado = cursor.fetchone()
    nome_aluno = resultado[0] if resultado else "Aluno"

    cursor.execute("""
        SELECT Turma.id_turma, Turma.nome, Turma.descricao, Turma.especialidade
        FROM Aluno_Turma
        JOIN Turma ON Aluno_Turma.id_turma = Turma.id_turma
        WHERE Aluno_Turma.id_aluno = ?
    """, (id_aluno,))
    turmas = cursor.fetchall()
    conn.close()

    win = tk.Toplevel()
    win.title("Ambiente do Aluno")
    win.geometry("700x500")

    tk.Label(win, text=f"Bem-vindo(a), {nome_aluno}", font=("Arial", 16)).pack(pady=10)

    frame_turmas = tk.Frame(win)
    frame_turmas.pack(expand=True, fill='both', padx=20, pady=10)

    for turma in turmas:
        frame_card = tk.Frame(frame_turmas, relief="raised", bd=2, padx=10, pady=10, bg="white")
        frame_card.pack(pady=8, fill="x")

        tk.Label(frame_card, text=turma[1], font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
        tk.Label(frame_card, text=f"{turma[2]} | {turma[3]}", font=("Arial", 11), bg="white").pack(anchor="w", pady=2)
        tk.Button(frame_card, text="Acessar", command=lambda tid=turma[0]: pagina_turma_aluno(tid)).pack(anchor="e", pady=5)

def pagina_turma_aluno(id_turma):
    conn = sqlite3.connect("escola.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Turma.nome, Turma.descricao, Turma.especialidade, Professor.nome
        FROM Turma
        JOIN Professor ON Turma.id_professor = Professor.id_professor
        WHERE Turma.id_turma = ?
    """, (id_turma,))
    info = cursor.fetchone()

    cursor.execute("""
        SELECT Aluno.nome FROM Aluno_Turma
        JOIN Aluno ON Aluno.id_aluno = Aluno_Turma.id_aluno
        WHERE Aluno_Turma.id_turma = ?
    """, (id_turma,))
    alunos = cursor.fetchall()

    conn.close()

    win = tk.Toplevel()
    win.title(f"Turma - {info[0]}")
    win.geometry("700x500")

    notebook = ttk.Notebook(win)
    notebook.pack(expand=True, fill="both")

   
    mural = ttk.Frame(notebook)
    notebook.add(mural, text="Mural")
    tk.Label(mural, text=f"{info[0]} - {info[2]}", font=("Arial", 14)).pack(pady=10)
    tk.Label(mural, text=f"Professor: {info[3]}", font=("Arial", 12)).pack(pady=5)
    tk.Message(mural, text=f"Descrição: {info[1]}", width=500, font=("Arial", 11)).pack(pady=10)

    
    pessoas = ttk.Frame(notebook)
    notebook.add(pessoas, text="Pessoas")
    tk.Label(pessoas, text=f"Professor: {info[3]}", font=("Arial", 12)).pack(pady=10)
    tk.Label(pessoas, text="Alunos:", font=("Arial", 12, "bold")).pack(pady=5)

    for aluno in alunos:
        tk.Label(pessoas, text=aluno[0], font=("Arial", 11)).pack()



root = tk.Tk()
root.title("Maestro - Conexão Musical")
root.geometry("600x400")

tk.Label(root, text="Bem-vindo ao Maestro!", font=("Arial", 16)).pack(pady=20)
tk.Button(root, text="Login", command=tela_login, width=20).pack(pady=10)
tk.Button(root, text="Cadastro", command=tela_cadastro, width=20).pack(pady=10)

root.mainloop()
