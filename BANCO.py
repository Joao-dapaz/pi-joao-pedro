import sqlite3

conn = sqlite3.connect("escola.db")
cursor = conn.cursor()

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
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Turma (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    especialidade TEXT,
    id_professor INTEGER NOT NULL,
    id_escola INTEGER NOT NULL,
    FOREIGN KEY (id_professor) REFERENCES Professor(id_professor),
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aluno (
    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    endereco TEXT,
    telefone TEXT,
    senha TEXT NOT NULL,
    id_escola INTEGER,
    FOREIGN KEY (id_escola) REFERENCES Escola(id_escola)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aluno_Turma (
    id_aluno INTEGER NOT NULL,
    id_turma INTEGER NOT NULL,
    PRIMARY KEY (id_aluno, id_turma),
    FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
    FOREIGN KEY (id_turma) REFERENCES Turma(id_turma)
)
""")

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
conn.commit()
conn.close()