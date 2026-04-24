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
    SELECT titulo, descricao, data_envio, id_turma, arquivo
    FROM Material
    WHERE id_professor = ?
    ORDER BY data_envio DESC
    """, (id_professor,))

    materiais = cursor.fetchall()
    conn.close()

    return materiais

def publicar_material(titulo, descricao, arquivo, data_envio, id_turma, id_professor):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Material (titulo, descricao, arquivo, data_envio, id_turma, id_professor)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, descricao, arquivo, data_envio, id_turma, id_professor))

    conn.commit()
    conn.close()

def listar_materiais():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT titulo, descricao, data_envio, id_turma, arquivo
    FROM Material
    ORDER BY data_envio DESC
    """)

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

def listar_turmas_do_aluno(id_aluno):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Turma.id_turma, Turma.nome, Turma.descricao, Professor.nome
    FROM Turma
    JOIN Professor ON Turma.id_professor = Professor.id_professor
    JOIN Aluno_Turma ON Turma.id_turma = Aluno_Turma.id_turma
    WHERE Aluno_Turma.id_aluno = ?
    """, (id_aluno,))

    turmas = cursor.fetchall()
    conn.close()

    return turmas

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
# ===== FUNÇÕES ADMIN_ESCOLA =====

def admin_login(email, senha):
    """Login do administrador da escola"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Admin_Escola WHERE email=? AND senha=?",
        (email, senha)
    )

    admin = cursor.fetchone()

    conn.close()

    return admin


def inserir_admin(nome, email, senha, endereco, telefone, id_escola):
    """Cria novo admin (quando escola se registra)"""
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Admin_Escola (nome, email, senha, endereco, telefone, id_escola, data_criacao, ativo)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), 1)
        """, (nome, email, senha, endereco, telefone, id_escola))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def buscar_admin(id_admin):
    """Busca dados de um admin específico"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Admin_Escola WHERE id_admin=?",
        (id_admin,)
    )

    admin = cursor.fetchone()

    conn.close()

    return admin
# ===== FUNÇÕES SOLICITACAO_ALUNO =====

def inserir_solicitacao_aluno(id_aluno, id_escola=None):
    """Cria solicitação de aluno pendente"""
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Solicitacao_Aluno (id_aluno, id_escola, status, data_solicitacao)
        VALUES (?, ?, 'pendente', datetime('now'))
        """, (id_aluno, id_escola))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def listar_solicitacoes_alunos(id_escola, status=None):
    """Lista solicitações de alunos da escola"""
    conn = conectar()
    cursor = conn.cursor()

    if status:
        cursor.execute("""
        SELECT Aluno.id_aluno, Aluno.nome, Aluno.email, Aluno.telefone, 
               Aluno.endereco, Solicitacao_Aluno.status, Solicitacao_Aluno.data_solicitacao
        FROM Aluno
        JOIN Solicitacao_Aluno ON Aluno.id_aluno = Solicitacao_Aluno.id_aluno
        WHERE Solicitacao_Aluno.id_escola = ? AND Solicitacao_Aluno.status = ?
        ORDER BY Solicitacao_Aluno.data_solicitacao DESC
        """, (id_escola, status))
    else:
        cursor.execute("""
        SELECT Aluno.id_aluno, Aluno.nome, Aluno.email, Aluno.telefone, 
               Aluno.endereco, Solicitacao_Aluno.status, Solicitacao_Aluno.data_solicitacao
        FROM Aluno
        JOIN Solicitacao_Aluno ON Aluno.id_aluno = Solicitacao_Aluno.id_aluno
        WHERE Solicitacao_Aluno.id_escola = ?
        ORDER BY Solicitacao_Aluno.data_solicitacao DESC
        """, (id_escola,))

    solicitacoes = cursor.fetchall()
    conn.close()

    return solicitacoes


def buscar_solicitacao_aluno(id_aluno, id_escola):
    """Busca solicitação específica de aluno"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM Solicitacao_Aluno
    WHERE id_aluno=? AND id_escola=?
    """, (id_aluno, id_escola))

    solicitacao = cursor.fetchone()

    conn.close()

    return solicitacao


def atualizar_status_aluno(id_aluno, novo_status):
    """Atualiza status_escola do aluno"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Aluno SET status_escola = ?, data_aprovacao = datetime('now')
    WHERE id_aluno = ?
    """, (novo_status, id_aluno))

    conn.commit()
    conn.close()


def atualizar_solicitacao_aluno(id_aluno, id_escola, novo_status, id_admin, mensagem_recusa=None):
    """Atualiza status da solicitação de aluno"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Solicitacao_Aluno 
    SET status = ?, id_admin_revisor = ?, data_revisao = datetime('now'), mensagem_recusa = ?
    WHERE id_aluno = ? AND id_escola = ?
    """, (novo_status, id_admin, mensagem_recusa, id_aluno, id_escola))

    conn.commit()
    conn.close()


def contar_alunos_por_status(id_escola, status):
    """Conta alunos por status"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM Solicitacao_Aluno
    WHERE id_escola = ? AND status = ?
    """, (id_escola, status))

    count = cursor.fetchone()[0]
    conn.close()

    return count
# ===== FUNÇÕES SOLICITACAO_PROFESSOR =====

def inserir_solicitacao_professor(id_professor, id_escola=None):
    """Cria solicitação de professor pendente"""
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Solicitacao_Professor (id_professor, id_escola, status, data_solicitacao)
        VALUES (?, ?, 'pendente', datetime('now'))
        """, (id_professor, id_escola))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False


def listar_solicitacoes_professores(id_escola, status=None):
    """Lista solicitações de professores da escola"""
    conn = conectar()
    cursor = conn.cursor()

    if status:
        cursor.execute("""
        SELECT Professor.id_professor, Professor.nome, Professor.email, Professor.telefone, 
               Professor.proficiencia, Solicitacao_Professor.status, Solicitacao_Professor.data_solicitacao
        FROM Professor
        JOIN Solicitacao_Professor ON Professor.id_professor = Solicitacao_Professor.id_professor
        WHERE Solicitacao_Professor.id_escola = ? AND Solicitacao_Professor.status = ?
        ORDER BY Solicitacao_Professor.data_solicitacao DESC
        """, (id_escola, status))
    else:
        cursor.execute("""
        SELECT Professor.id_professor, Professor.nome, Professor.email, Professor.telefone, 
               Professor.proficiencia, Solicitacao_Professor.status, Solicitacao_Professor.data_solicitacao
        FROM Professor
        JOIN Solicitacao_Professor ON Professor.id_professor = Solicitacao_Professor.id_professor
        WHERE Solicitacao_Professor.id_escola = ?
        ORDER BY Solicitacao_Professor.data_solicitacao DESC
        """, (id_escola,))

    solicitacoes = cursor.fetchall()
    conn.close()

    return solicitacoes


def buscar_solicitacao_professor(id_professor, id_escola):
    """Busca solicitação específica de professor"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM Solicitacao_Professor
    WHERE id_professor=? AND id_escola=?
    """, (id_professor, id_escola))

    solicitacao = cursor.fetchone()

    conn.close()

    return solicitacao


def atualizar_status_professor(id_professor, novo_status):
    """Atualiza status_escola do professor"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Professor SET status_escola = ?, data_aprovacao = datetime('now')
    WHERE id_professor = ?
    """, (novo_status, id_professor))

    conn.commit()
    conn.close()


def atualizar_solicitacao_professor(id_professor, id_escola, novo_status, id_admin, mensagem_recusa=None):
    """Atualiza status da solicitação de professor"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Solicitacao_Professor 
    SET status = ?, id_admin_revisor = ?, data_revisao = datetime('now'), mensagem_recusa = ?
    WHERE id_professor = ? AND id_escola = ?
    """, (novo_status, id_admin, mensagem_recusa, id_professor, id_escola))

    conn.commit()
    conn.close()


def contar_professores_por_status(id_escola, status):
    """Conta professores por status"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM Solicitacao_Professor
    WHERE id_escola = ? AND status = ?
    """, (id_escola, status))

    count = cursor.fetchone()[0]
    conn.close()

    return count
# ===== FUNÇÕES AVISO_ESCOLA =====

def inserir_aviso(titulo, conteudo, prioridade, arquivo, id_admin, id_escola):
    """Insere novo aviso"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Aviso_Escola (titulo, conteudo, prioridade, arquivo, id_admin, id_escola, data_criacao, ativo)
    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), 1)
    """, (titulo, conteudo, prioridade, arquivo, id_admin, id_escola))

    conn.commit()
    id_aviso = cursor.lastrowid
    conn.close()

    return id_aviso


def listar_avisos_escola(id_escola):
    """Lista todos os avisos da escola (ativo)"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_aviso, titulo, conteudo, prioridade, arquivo, id_admin, data_criacao, data_atualizacao
    FROM Aviso_Escola
    WHERE id_escola = ? AND ativo = 1
    ORDER BY data_criacao DESC
    """, (id_escola,))

    avisos = cursor.fetchall()
    conn.close()

    return avisos


def buscar_aviso(id_aviso):
    """Busca aviso específico"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Aviso_Escola WHERE id_aviso=?",
        (id_aviso,)
    )

    aviso = cursor.fetchone()

    conn.close()

    return aviso


def atualizar_aviso(id_aviso, titulo, conteudo, prioridade, arquivo):
    """Atualiza aviso existente"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Aviso_Escola
    SET titulo = ?, conteudo = ?, prioridade = ?, arquivo = ?, data_atualizacao = datetime('now')
    WHERE id_aviso = ?
    """, (titulo, conteudo, prioridade, arquivo, id_aviso))

    conn.commit()
    conn.close()


def deletar_aviso(id_aviso):
    """Deleta aviso (soft delete)"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Aviso_Escola SET ativo = 0 WHERE id_aviso = ?
    """, (id_aviso,))

    conn.commit()
    conn.close()
# ===== FUNÇÕES AUXILIARES PARA DASHBOARD =====

def contar_turmas(id_escola):
    """Conta turmas da escola"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM Turma WHERE id_escola = ?",
        (id_escola,)
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count


def contar_materiais(id_escola):
    """Conta materiais publicados na escola"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM Material
    WHERE id_turma IN (SELECT id_turma FROM Turma WHERE id_escola = ?)
    """, (id_escola,))

    count = cursor.fetchone()[0]
    conn.close()

    return count


def buscar_aluno(id_aluno):
    """Busca dados completos de um aluno"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Aluno WHERE id_aluno = ?",
        (id_aluno,)
    )

    aluno = cursor.fetchone()
    conn.close()

    return aluno


def buscar_professor(id_professor):
    """Busca dados completos de um professor"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Professor WHERE id_professor = ?",
        (id_professor,)
    )

    professor = cursor.fetchone()
    conn.close()

    return professor

# ===== FUNÇÕES TURMA (Admin) =====

def inserir_turma(nome, descricao, especialidade, id_professor, id_escola, criada_por='professor'):
    """Insere nova turma (admin ou professor)"""
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Turma (nome, descricao, especialidade, id_professor, id_escola, criada_por, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """, (nome, descricao, especialidade, id_professor, id_escola, criada_por))

        conn.commit()
        id_turma = cursor.lastrowid
        conn.close()

        return id_turma

    except sqlite3.IntegrityError:
        conn.close()
        return False


def atualizar_turma(id_turma, nome, descricao, especialidade, id_professor):
    """Atualiza turma existente"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE Turma
    SET nome = ?, descricao = ?, especialidade = ?, id_professor = ?
    WHERE id_turma = ?
    """, (nome, descricao, especialidade, id_professor, id_turma))

    conn.commit()
    conn.close()


def deletar_turma(id_turma):
    """Deleta turma"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM Turma WHERE id_turma = ?
    """, (id_turma,))

    conn.commit()
    conn.close()


def listar_professores_aprovados(id_escola):
    """Lista professores aprovados da escola (para dropdown ao criar turma)"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id_professor, nome
    FROM Professor
    WHERE id_escola = ? AND status_escola = 'aprovado'
    ORDER BY nome
    """, (id_escola,))

    professores = cursor.fetchall()
    conn.close()

    return professores

def buscar_turma(id_turma):
    """Busca dados completos de uma turma"""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Turma WHERE id_turma = ?",
        (id_turma,)
    )

    turma = cursor.fetchone()
    conn.close()

    return turma