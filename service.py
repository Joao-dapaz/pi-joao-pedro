import model

def buscar_dados_turmas_aluno(id_aluno, id_escola):

    turmas = model.listar_turmas_do_aluno(id_aluno)
    escola = model.buscar_escola(id_escola)
    materiais = model.listar_materiais()

    materiais_por_turma = {}

    for m in materiais:
        id_turma = m[3]

        if id_turma not in materiais_por_turma:
            materiais_por_turma[id_turma] = []

        materiais_por_turma[id_turma].append(m)

    return turmas, escola, materiais_por_turma


def buscar_pessoas_da_turma(id_turma, session):

    professor, alunos = model.listar_pessoas_da_turma(id_turma)

    if professor is None:
        return "Turma não encontrada", 404

    nome_turma = model.buscar_nome_turma(id_turma)

    origem = "aluno"
    if "professor_id" in session:
        origem = "professor"

    return {
        "nome_turma": nome_turma,
        "professor": professor,
        "alunos": alunos,
        "origem": origem
    }


# ===== AUTENTICAÇÃO =====

def fazer_login_aluno(email, senha):
    aluno = model.aluno_login(email, senha)

    if not aluno:
        return {"sucesso": False, "mensagem": "Email ou senha inválidos."}

    if aluno[6] is None:
        return {"sucesso": False, "mensagem": "Você precisa se conectar a uma escola antes de entrar."}

    return {
        "sucesso": True,
        "aluno_id": aluno[0],
        "id_escola": aluno[6]
    }


def fazer_login_professor(email, senha):
    professor = model.professor_login(email, senha)

    if not professor:
        return {"sucesso": False, "mensagem": "Email ou senha inválidos."}

    return {
        "sucesso": True,
        "professor_id": professor[0],
        "id_escola": professor[7]
    }


def fazer_login_admin(email, senha):
    admin = model.admin_login(email, senha)

    if not admin:
        return {"sucesso": False, "mensagem": "Email ou senha inválidos."}

    return {
        "sucesso": True,
        "admin_id": admin[0],
        "id_escola": admin[7]
    }


# ===== MATERIAIS =====

def publicar_material_professor(titulo, descricao, arquivo, id_turma, id_professor):
    from datetime import date

    if not titulo or not titulo.strip():
        return {"sucesso": False, "mensagem": "O título é obrigatório."}

    if not descricao or not descricao.strip():
        return {"sucesso": False, "mensagem": "A descrição é obrigatória."}

    data_envio = date.today().isoformat()

    model.publicar_material(titulo, descricao, arquivo, data_envio, int(id_turma), id_professor)

    return {"sucesso": True}


# ===== DASHBOARD ADMIN =====

def buscar_dashboard_admin(id_escola):
    stats = {
        "total_alunos_aprovados":      model.contar_alunos_por_status(id_escola, 'aprovado'),
        "total_alunos_pendentes":      model.contar_alunos_por_status(id_escola, 'pendente'),
        "total_alunos_rejeitados":     model.contar_alunos_por_status(id_escola, 'rejeitado'),
        "total_professores_aprovados": model.contar_professores_por_status(id_escola, 'aprovado'),
        "total_professores_pendentes": model.contar_professores_por_status(id_escola, 'pendente'),
        "total_professores_rejeitados":model.contar_professores_por_status(id_escola, 'rejeitado'),
        "total_turmas":                model.contar_turmas(id_escola),
        "total_materiais":             model.contar_materiais(id_escola),
    }
    return stats


# ===== SOLICITAÇÕES ALUNOS =====

def listar_solicitacoes_alunos(id_escola, status=None):
    return model.listar_solicitacoes_alunos(id_escola, status)


def aprovar_aluno(id_aluno, id_escola, id_admin):
    model.atualizar_status_aluno(id_aluno, 'aprovado')
    model.atualizar_solicitacao_aluno(id_aluno, id_escola, 'aprovado', id_admin)

    aluno = model.buscar_aluno(id_aluno)
    enviar_email_aprovacao('aluno', aluno[2], aluno[1])


def rejeitar_aluno(id_aluno, id_escola, id_admin, mensagem=""):
    model.atualizar_status_aluno(id_aluno, 'rejeitado')
    model.atualizar_solicitacao_aluno(id_aluno, id_escola, 'rejeitado', id_admin, mensagem)

    aluno = model.buscar_aluno(id_aluno)
    enviar_email_rejeicao('aluno', aluno[2], aluno[1], mensagem)


# ===== SOLICITAÇÕES PROFESSORES =====

def listar_solicitacoes_professores(id_escola, status=None):
    return model.listar_solicitacoes_professores(id_escola, status)


def aprovar_professor(id_professor, id_escola, id_admin):
    model.atualizar_status_professor(id_professor, 'aprovado')
    model.atualizar_solicitacao_professor(id_professor, id_escola, 'aprovado', id_admin)

    professor = model.buscar_professor(id_professor)
    enviar_email_aprovacao('professor', professor[2], professor[1])


def rejeitar_professor(id_professor, id_escola, id_admin, mensagem=""):
    model.atualizar_status_professor(id_professor, 'rejeitado')
    model.atualizar_solicitacao_professor(id_professor, id_escola, 'rejeitado', id_admin, mensagem)

    professor = model.buscar_professor(id_professor)
    enviar_email_rejeicao('professor', professor[2], professor[1], mensagem)


# ===== AVISOS =====

def criar_aviso(titulo, conteudo, prioridade, arquivo, id_admin, id_escola):
    return model.inserir_aviso(titulo, conteudo, prioridade, arquivo, id_admin, id_escola)


def editar_aviso(id_aviso, titulo, conteudo, prioridade, arquivo):
    model.atualizar_aviso(id_aviso, titulo, conteudo, prioridade, arquivo)


def deletar_aviso(id_aviso):
    model.deletar_aviso(id_aviso)


def listar_avisos(id_escola):
    return model.listar_avisos_escola(id_escola)


# ===== TURMAS (Admin) =====

def criar_turma_admin(nome, descricao, especialidade, id_professor, id_escola):
    return model.inserir_turma(nome, descricao, especialidade, id_professor, id_escola, criada_por='admin')


def editar_turma(id_turma, nome, descricao, especialidade, id_professor):
    model.atualizar_turma(id_turma, nome, descricao, especialidade, id_professor)


def deletar_turma(id_turma):
    model.deletar_turma(id_turma)


def listar_professores_aprovados(id_escola):
    return model.listar_professores_aprovados(id_escola)


# ===== EMAIL =====
# As funções de envio de email são simuladas com prints, mas podem ser implementadas usando SMTP ou serviços como SendGrid.
# ainda não sei se prossigo implementar o envio real de email, mas deixei a estrutura pronta para isso.

def enviar_email_aprovacao(tipo_usuario, email, nome):
    assunto = "Sua solicitação foi aprovada!"

    if tipo_usuario == 'aluno':
        corpo = f"""
Olá {nome},

Sua solicitação para participar da escola foi aprovada com sucesso!

Você agora pode fazer login na plataforma Maestro.

Após o login, você poderá escolher suas turmas.

Bem-vindo!

Maestro - Conexões Musicais
        """
    else:
        corpo = f"""
Olá {nome},

Sua solicitação para ser professor foi aprovada com sucesso!

Você agora pode fazer login na plataforma Maestro e começar a gerenciar suas turmas.

Bem-vindo!

Maestro - Conexões Musicais
        """

    # TODO: Implementar envio real de email (SMTP ou SendGrid)
    print(f"[EMAIL] Para: {email}\nAssunto: {assunto}\n\n{corpo}")


def enviar_email_rejeicao(tipo_usuario, email, nome, mensagem):
    assunto = "Sua solicitação foi rejeitada"

    if tipo_usuario == 'aluno':
        corpo = f"""
Olá {nome},

Sua solicitação para participar da escola foi analisada e infelizmente foi rejeitada.

Motivo da rejeição:
{mensagem}

Se tiver dúvidas, entre em contato conosco.

Maestro - Conexões Musicais
        """
    else:
        corpo = f"""
Olá {nome},

Sua solicitação para ser professor foi analisada e infelizmente foi rejeitada.

Motivo da rejeição:
{mensagem}

Se tiver dúvidas, entre em contato conosco.

Maestro - Conexões Musicais
        """

    # TODO: Implementar envio real de email (SMTP ou SendGrid)
    print(f"[EMAIL] Para: {email}\nAssunto: {assunto}\n\n{corpo}")