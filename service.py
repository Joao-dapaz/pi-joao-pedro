import model

def buscar_dados_turmas_aluno(id_aluno,id_escola):

    turmas= model.listar_turmas_do_aluno(id_aluno)
    escola= model.buscar_escola(id_escola)
    materiais= model.listar_materiais()

    materiais_por_turma = {}

    for m in materiais:
        id_turma = m[3]

        if id_turma not in materiais_por_turma:
            materiais_por_turma[id_turma] = []

        materiais_por_turma[id_turma].append(m)

    return turmas, escola, materiais_por_turma
    
def buscar_pessoas_da_turma(id_turma,session):

    professor, alunos = model.listar_pessoas_da_turma(id_turma)

    if professor is None:
        return "Turma não encontrada", 404
    
    nome_turma = model.buscar_nome_turma(id_turma)

    origem = "aluno"
    if "professor_id" in session:
        origem = "professor"
        
    return {
        "nome_turma":nome_turma,
        "professor":professor,
        "alunos":alunos,
        "origem":origem
    }
