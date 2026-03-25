import sqlite3


def conectar():
    return sqlite3.connect("escola.db")


def aluno_login(email, senha):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Aluno WHERE email=? AND senha=?",
        (email, senha)
    )

    aluno = cursor.fetchone()

    conn.close()

    return aluno

def professor_login(email, senha):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Professor WHERE email=? AND senha=?",
        (email, senha)
    )

    professor = cursor.fetchone()

    conn.close()

    return professor


def cadastro_aluno(nome, email, endereco, telefone, senha, id_escola):

    conn = conectar()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO Aluno
        (nome, email, endereco, telefone, senha, id_escola)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, email, endereco, telefone, senha, id_escola))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()
        return False


def listar_turmas_do_professor(id_professor):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_turma, nome, descricao
    FROM Turma
    WHERE id_professor = ?
    """, (id_professor,))

    turmas = cursor.fetchall()

    conn.close()

    return turmas

def listar_materiais_professor(id_professor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT titulo, descricao, data_envio, id_turma
    FROM Material
    WHERE id_professor = ?
    ORDER BY data_envio DESC
    """, (id_professor,))

    materiais = cursor.fetchall()
    conn.close()

    return materiais

def buscar_escola(id_escola):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome, descricao, endereco, telefone
    FROM Escola
    WHERE id_escola = ?
    """, (id_escola,))

    escola = cursor.fetchone()

    conn.close()

    return escola


def listar_turmas_por_escola(id_escola):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Turma.id_turma, Turma.nome, Turma.descricao, Professor.nome
    FROM Turma
    JOIN Professor ON Turma.id_professor = Professor.id_professor
    WHERE Turma.id_escola = ?
    """, (id_escola,))

    turmas = cursor.fetchall()

    conn.close()

    return turmas


def listar_pessoas_da_turma(id_turma):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Professor.nome
    FROM Turma
    JOIN Professor ON Turma.id_professor = Professor.id_professor
    WHERE Turma.id_turma = ?
    """, (id_turma,))

    professor = cursor.fetchone()

    cursor.execute("""
    SELECT Aluno.nome
    FROM Aluno
    JOIN Aluno_Turma
    ON Aluno.id_aluno = Aluno_Turma.id_aluno
    WHERE Aluno_Turma.id_turma = ?
    """, (id_turma,))

    alunos = cursor.fetchall()

    conn.close()

    return professor[0] if professor else None, [a[0] for a in alunos]


def buscar_nome_turma(id_turma):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome
    FROM Turma
    WHERE id_turma = ?
    """, (id_turma,))

    turma = cursor.fetchone()

    conn.close()

    return turma[0] if turma else None

def listar_escolas():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_escola, nome, endereco, latitude, longitude, telefone, descricao
    FROM Escola
    """)

    escolas = cursor.fetchall()

    conn.close()

    return escolas