import sqlite3

conn = sqlite3.connect("escola.db")
cursor = conn.cursor()

# ESCOLAS
escolas = [
("Escola 1","notavel@escola.com","senha321","Av. Érico Veríssimo, 595",-30.049152728961868,-51.21874701123376,"5199990004","Escola de bateria"),
("Escola 2","harmonica@escola.com","senha654","Av. Protásio Alves, 1650",-30.041015752771376,-51.19154753938872,"5199990005","Estudos em teoria musical"),
("Escola 3","acorde@escola.com","senha987","Av. Cristóvão Colombo, 545",-30.023333538082234,-51.21215625849747,"5199990006","Especialização em cordas"),
("Instituto de Música da EST","est@musica.com","senha123","Rua Amadeo Rossi, 467",-30.03464289127531,-51.21774238491852,"5199990001","Formação musical completa"),
("Escola de Música Moinhos","moinhos@musica.com","senha123","Rua Padre Chagas, 145",-30.02773158490218,-51.20351294762133,"5199990002","Aulas de instrumentos e teoria"),
("Studio Som Escola de Música","studiosom@musica.com","senha123","Av. João Pessoa, 1050",-30.04631277419566,-51.22498356127044,"5199990003","Cursos práticos e gravação"),
("Escola de Música Opus","opus@musica.com","senha123","Av. Protásio Alves, 3490",-30.05841293784527,-51.17481256399811,"5199990004","Especializada em formação profissional"),
("Escola de Música Cordas & Acordes","cordas@musica.com","senha123","Rua 24 de Outubro, 850",-30.01294361588274,-51.20127894755236,"5199990005","Foco em instrumentos de corda")
]

for escola in escolas:
    cursor.execute("""
    INSERT OR IGNORE INTO Escola
    (nome,email,senha,endereco,latitude,longitude,telefone,descricao)
    VALUES (?,?,?,?,?,?,?,?)
    """, escola)


# PROFESSORES
professores = [
("Marcos Silva","marcos@escola1.com","senha123","Rua A,100","5199990001","Violão",1),
("Ana Rocha","ana@escola2.com","senha123","Rua B,200","5199990002","Canto",2),
("Pedro Martins","pedro@escola3.com","senha123","Rua C,300","5199990003","Teclado",3)
]

for professor in professores:
    cursor.execute("""
    INSERT OR IGNORE INTO Professor
    (nome,email,senha,endereco,telefone,proficiencia,id_escola)
    VALUES (?,?,?,?,?,?,?)
    """, professor)


# TURMAS
turmas = [
("Violão Avançado","Aulas focadas em técnica e repertório.","Violão",1,1),
("Canto Iniciante","Introdução ao canto e respiração.","Canto",2,2),
("Teclado Intermediário","Leitura musical e harmonização.","Teclado",3,3),

("Guitarra Rock","Técnicas de guitarra elétrica e solos.","Guitarra",1,1),
("Bateria Básica","Ritmos fundamentais para iniciantes.","Bateria",1,1),
("Percepção Musical","Treino auditivo e intervalos.","Percepção",1,1),

("Piano Clássico","Repertório erudito.","Piano",2,2),
("Coral Adulto","Canto em grupo.","Coral",2,2),
("Violino Iniciante","Postura e afinação.","Violino",2,2),

("Saxofone Jazz","Improvisação e swing.","Saxofone",3,3),
("Contrabaixo","Walking bass e groove.","Contrabaixo",3,3),
("Produção Musical","Gravação e mixagem.","Produção",3,3)
]

for turma in turmas:
    cursor.execute("""
    INSERT OR IGNORE INTO Turma
    (nome,descricao,especialidade,id_professor,id_escola)
    VALUES (?,?,?,?,?)
    """, turma)


# ALUNOS (AGORA COM id_escola)
alunos = [
("Rafael Batista","rafael@aluno.com","Rua do Sol 4","5199000004","abc",1),
("Juliana Martins","juliana@aluno.com","Rua da Lua 5","5199000005","def",1),
("Carlos Silva","carlos@aluno.com","Rua das Estrelas 6","5199000006","ghi",2),
("Larissa Monteiro","larissa@aluno.com","Rua Vento 7","5199000007","jkl",2),
("Gustavo Rocha","gustavo@aluno.com","Rua Fogo 8","5199000008","mno",3),
("Beatriz Torres","beatriz@aluno.com","Rua Chuva 9","5199000009","pqr",3),
("Felipe Luz","felipe@aluno.com","Rua Neve 10","5199000010","stu",1),
("Camila Andrade","camila@aluno.com","Rua Mar 11","5199000011","vwx",2),
("Vinícius Mendes","vinicius@aluno.com","Rua Serra 12","5199000012","yz1",3),
("Sofia Nunes","sofia@aluno.com","Rua Luar 13","5199000013","234",1)
]

for aluno in alunos:
    cursor.execute("""
    INSERT OR IGNORE INTO Aluno
    (nome,email,endereco,telefone,senha,id_escola)
    VALUES (?,?,?,?,?,?)
    """, aluno)


# RELAÇÃO ALUNO-TURMA
relacoes = [
(1,1),
(2,1),
(3,2),
(4,2),
(5,3),
(6,3),
(7,4),
(8,7),
(9,10),
(10,5)
]

for relacao in relacoes:
    cursor.execute("""
    INSERT OR IGNORE INTO Aluno_Turma
    (id_aluno,id_turma)
    VALUES (?,?)
    """, relacao)


conn.commit()
conn.close()