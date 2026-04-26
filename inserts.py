import sqlite3

conn = sqlite3.connect("escola.db")
cursor = conn.cursor()

def inserir(query, dados):
    try:
        cursor.execute(query, dados)
    except sqlite3.IntegrityError as e:
        print(f"Erro ao inserir: {dados} -> {e}")


# ===== ESCOLAS =====
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
    inserir("""
    INSERT INTO Escola
    (nome,email,senha,endereco,latitude,longitude,telefone,descricao)
    VALUES (?,?,?,?,?,?,?,?)
    """, escola)


# ===== ADMINS =====
admins = [
("João Admin 1","admin1@escola.com","senha123","Av. Érico Veríssimo, 595","5199990004",1),
("João Admin 2","admin2@escola.com","senha123","Av. Protásio Alves, 1650","5199990005",2),
("João Admin 3","admin3@escola.com","senha123","Av. Cristóvão Colombo, 545","5199990006",3),
("João Admin EST","est.admin@musica.com","senha123","Rua Amadeo Rossi, 467","5199990001",4),
("João Admin Moinhos","moinhos.admin@musica.com","senha123","Rua Padre Chagas, 145","5199990002",5),
("João Admin StudioSom","studiosom.admin@musica.com","senha123","Av. João Pessoa, 1050","5199990003",6),
("João Admin Opus","opus.admin@musica.com","senha123","Av. Protásio Alves, 3490","5199990004",7),
("João Admin Cordas","cordas.admin@musica.com","senha123","Rua 24 de Outubro, 850","5199990005",8)
]

for admin in admins:
    inserir("""
    INSERT INTO Admin_Escola
    (nome,email,senha,endereco,telefone,id_escola,data_criacao)
    VALUES (?,?,?,?,?,?,datetime('now'))
    """, admin)


professores = [
# aprovados
("Marcos Silva","marcos@escola1.com","senha123","Rua A,100","5199990001","Violão",1,"aprovado"),

# pendentes
("Carlos Novo","carlos@prof.com","123","Rua X","5199991111","Guitarra",1,"pendente"),
("Fernanda Nova","fernanda@prof.com","123","Rua Y","5199992222","Canto",2,"pendente"),
("Ricardo Novo","ricardo@prof.com","123","Rua Z","5199993333","Bateria",3,"pendente")
]

for prof in professores:
    inserir("""
    INSERT INTO Professor
    (nome,email,senha,endereco,telefone,proficiencia,id_escola,status_escola)
    VALUES (?,?,?,?,?,?,?,?)
    """, prof)

solicitacoes_professores = [
(1,1,'aprovado'),

(2,1,'pendente'),
(3,2,'pendente'),
(4,3,'pendente')
]

for sol in solicitacoes_professores:
    inserir("""
    INSERT INTO Solicitacao_Professor
    (id_professor,id_escola,status,data_solicitacao)
    VALUES (?,?,?,datetime('now'))
    """, sol)
    
# ===== TURMAS =====
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
    inserir("""
    INSERT INTO Turma
    (nome,descricao,especialidade,id_professor,id_escola)
    VALUES (?,?,?,?,?)
    """, turma)


alunos = [
# aprovados
("Rafael Batista","rafael@aluno.com","Rua do Sol 4","5199000004","abc",1,"aprovado"),
("Juliana Martins","juliana@aluno.com","Rua da Lua 5","5199000005","def",1,"aprovado"),

# pendentes
("Lucas Teste","lucas@aluno.com","Rua A","5199000014","123",1,"pendente"),
("Marina Teste","marina@aluno.com","Rua B","5199000015","123",1,"pendente"),
("João Teste","joaoteste@aluno.com","Rua C","5199000016","123",2,"pendente"),
("Ana Teste","anateste@aluno.com","Rua D","5199000017","123",2,"pendente"),
("Pedro Teste","pedroteste@aluno.com","Rua E","5199000018","123",3,"pendente"),
("Carla Teste","carlateste@aluno.com","Rua F","5199000019","123",3,"pendente")
]

for aluno in alunos:
    inserir("""
    INSERT INTO Aluno
    (nome,email,endereco,telefone,senha,id_escola,status_escola)
    VALUES (?,?,?,?,?,?,?)
    """, aluno)

solicitacoes_alunos = [
# aprovados
(1,1,'aprovado'),
(2,1,'aprovado'),

# pendentes
(3,1,'pendente'),
(4,1,'pendente'),
(5,2,'pendente'),
(6,2,'pendente'),
(7,3,'pendente'),
(8,3,'pendente')
]

for sol in solicitacoes_alunos:
    inserir("""
    INSERT INTO Solicitacao_Aluno
    (id_aluno,id_escola,status,data_solicitacao)
    VALUES (?,?,?,datetime('now'))
    """, sol)

# ===== RELAÇÃO ALUNO-TURMA =====
relacoes = [
(1,1),(2,1),(3,2),(4,2),(5,3),
(6,3),(7,4),(8,7),(9,10),(10,5)
]

for rel in relacoes:
    inserir("""
    INSERT INTO Aluno_Turma
    (id_aluno,id_turma)
    VALUES (?,?)
    """, rel)


# ===== MATERIAIS =====
materiais_lista = [
("Aula 1 - Acordes básicos", "Introdução aos acordes maiores.", None, "2026-03-20", 1, 1),
("Exercício de ritmo", "Treinar batidas simples.", None, "2026-03-21", 1, 1),
("Técnica vocal", "Exercícios de respiração.", None, "2026-03-20", 2, 2),
("Escalas no teclado", "Prática de escalas maiores.", None, "2026-03-22", 3, 3),
("Solo iniciante", "Primeiros solos na guitarra.", None, "2026-03-23", 4, 1),
("Coordenação motora", "Exercícios básicos de bateria.", None, "2026-03-23", 5, 1),
("Leitura musical", "Introdução à partitura.", None, "2026-03-21", 7, 2),
("Improvisação jazz", "Escalas e improviso.", None, "2026-03-22", 10, 3)
]

for mat in materiais_lista:
    inserir("""
    INSERT INTO Material
    (titulo, descricao, arquivo, data_envio, id_turma, id_professor)
    VALUES (?, ?, ?, ?, ?, ?)
    """, mat)


# ===== AVISOS =====
avisos = [
("Bem-vindo!", "Bem-vindo à plataforma Maestro. Nossas aulas começam em breve!", "normal", None, 1, 1),
("Importante", "Lembrete: comparecer 10 minutos antes da aula", "urgente", None, 1, 1),
("Aviamento de Boletos", "Os boletos estão disponíveis no sistema", "normal", None, 2, 2),
]

for aviso in avisos:
    inserir("""
    INSERT INTO Aviso_Escola
    (titulo,conteudo,prioridade,arquivo,id_escola,id_admin,data_criacao)
    VALUES (?,?,?,?,?,?,datetime('now'))
    """, aviso)


conn.commit()
conn.close()

print("Banco populado com sucesso.")