import sqlite3
from model import conectar

conn = conectar()
cursor = conn.cursor()

# ===== ESCOLA =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Escola (
    id_escola INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    endereco TEXT,
    latitude REAL,
    longitude REAL,
    telefone TEXT,
    descricao TEXT
)
""")

# ===== PROFESSOR =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Professor (
    id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    endereco TEXT,
    telefone TEXT,
    proficiencia TEXT,
    id_escola INTEGER NOT NULL,
    status_escola TEXT DEFAULT 'pendente',
    data_aprovacao TEXT,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

# ===== TURMA =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Turma (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    especialidade TEXT,
    id_professor INTEGER NOT NULL,
    id_escola INTEGER NOT NULL,
    criada_por TEXT DEFAULT 'professor',
    data_criacao TEXT,
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

# ===== ALUNO =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    endereco TEXT,
    telefone TEXT,
    senha TEXT NOT NULL,
    id_escola INTEGER,
    status_escola TEXT DEFAULT 'pendente',
    data_aprovacao TEXT,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

# ===== RELAÇÃO ALUNO-TURMA =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Aluno_Turma (
    id_aluno INTEGER NOT NULL,
    id_turma INTEGER NOT NULL,
    PRIMARY KEY (id_aluno, id_turma),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma)
)
""")

# ===== MATERIAL =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Material (
    id_material INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    arquivo TEXT,
    data_envio TEXT,
    id_turma INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor)
)
""")

# ===== ADMIN =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Admin_Escola (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    endereco TEXT,
    telefone TEXT,
    foto TEXT,
    id_escola INTEGER NOT NULL UNIQUE,
    data_criacao TEXT,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

# ===== AVISO =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Aviso_Escola (
    id_aviso INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    conteudo TEXT NOT NULL,
    prioridade TEXT CHECK(prioridade IN ('normal', 'urgente')),
    arquivo TEXT,
    id_escola INTEGER NOT NULL,
    id_admin INTEGER NOT NULL,
    data_criacao TEXT,
    data_atualizacao TEXT,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola),
    FOREIGN KEY (id_admin) REFERENCES Admin_Escola(id_admin)
)
""")

# ===== SOLICITAÇÃO ALUNO =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Solicitacao_Aluno (
    id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_aluno INTEGER NOT NULL,
    id_escola INTEGER,
    status TEXT CHECK(status IN ('pendente', 'aprovado', 'rejeitado')),
    mensagem_recusa TEXT,
    data_solicitacao TEXT,
    data_revisao TEXT,
    id_admin_revisor INTEGER,
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola),
    FOREIGN KEY (id_admin_revisor) REFERENCES Admin_Escola(id_admin)
)
""")

# ===== SOLICITAÇÃO PROFESSOR =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS Solicitacao_Professor (
    id_solicitacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_professor INTEGER NOT NULL,
    id_escola INTEGER,
    status TEXT CHECK(status IN ('pendente', 'aprovado', 'rejeitado')),
    mensagem_recusa TEXT,
    data_solicitacao TEXT,
    data_revisao TEXT,
    id_admin_revisor INTEGER,
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola),
    FOREIGN KEY (id_admin_revisor) REFERENCES Admin_Escola(id_admin)
)
""")

conn.commit()
conn.close()