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
    """Login de professor"""
    professor = model.professor_login(email, senha)
    
    if not professor:
        return {"sucesso": False, "mensagem": "Email ou senha inválidos."}
    
    return {
        "sucesso": True,
        "professor_id": professor[0],
        "id_escola": professor[7]  
    }
# ===== AUTENTICAÇÃO ADMIN =====

def fazer_login_admin(email, senha):
    """Login do administrador da escola"""
    admin = model.admin_login(email, senha)
    
    if not admin:
        return {"sucesso": False, "mensagem": "Email ou senha inválidos."}
    
    return {
        "sucesso": True,
        "admin_id": admin[0],
        "id_escola": admin[8]
    }


# ===== DASHBOARD ADMIN =====

def buscar_dashboard_admin(id_escola):
    """Retorna todos os dados para o dashboard"""
    stats = {
        "total_alunos_aprovados": model.contar_alunos_por_status(id_escola, 'aprovado'),
        "total_alunos_pendentes": model.contar_alunos_por_status(id_escola, 'pendente'),
        "total_alunos_rejeitados": model.contar_alunos_por_status(id_escola, 'rejeitado'),
        "total_professores_aprovados": model.contar_professores_por_status(id_escola, 'aprovado'),
        "total_professores_pendentes": model.contar_professores_por_status(id_escola, 'pendente'),
        "total_professores_rejeitados": model.contar_professores_por_status(id_escola, 'rejeitado'),
        "total_turmas": model.contar_turmas(id_escola),
        "total_materiais": model.contar_materiais(id_escola),
    }
    return stats


# ===== SOLICITAÇÕES ALUNOS =====

def listar_solicitacoes_alunos(id_escola, status=None):
    """Lista solicitações de alunos"""
    return model.listar_solicitacoes_alunos(id_escola, status)


def revisar_aluno(id_aluno, id_escola):
    """Retorna detalhes do aluno para revisão"""
    aluno = model.buscar_aluno(id_aluno)
    solicitacao = model.buscar_solicitacao_aluno(id_aluno, id_escola)
    return {"aluno": aluno, "solicitacao": solicitacao}


def aprovar_aluno(id_aluno, id_escola, id_admin):
    """Aprova um aluno"""
    model.atualizar_status_aluno(id_aluno, 'aprovado')
    model.atualizar_solicitacao_aluno(id_aluno, id_escola, 'aprovado', id_admin)
    
    # Envia email
    aluno = model.buscar_aluno(id_aluno)
    enviar_email_aprovacao('aluno', aluno[3], aluno[1])


def rejeitar_aluno(id_aluno, id_escola, id_admin, mensagem=""):
    """Rejeita um aluno"""
    model.atualizar_status_aluno(id_aluno, 'rejeitado')
    model.atualizar_solicitacao_aluno(id_aluno, id_escola, 'rejeitado', id_admin, mensagem)
    
    # Envia email
    aluno = model.buscar_aluno(id_aluno)
    enviar_email_rejeicao('aluno', aluno[3], aluno[1], mensagem)


# ===== SOLICITAÇÕES PROFESSORES =====

def listar_solicitacoes_professores(id_escola, status=None):
    """Lista solicitações de professores"""
    return model.listar_solicitacoes_professores(id_escola, status)


def revisar_professor(id_professor, id_escola):
    """Retorna detalhes do professor para revisão"""
    professor = model.buscar_professor(id_professor)
    solicitacao = model.buscar_solicitacao_professor(id_professor, id_escola)
    return {"professor": professor, "solicitacao": solicitacao}


def aprovar_professor(id_professor, id_escola, id_admin):
    """Aprova um professor"""
    model.atualizar_status_professor(id_professor, 'aprovado')
    model.atualizar_solicitacao_professor(id_professor, id_escola, 'aprovado', id_admin)
    
    # Envia email
    professor = model.buscar_professor(id_professor)
    enviar_email_aprovacao('professor', professor[3], professor[1])


def rejeitar_professor(id_professor, id_escola, id_admin, mensagem=""):
    """Rejeita um professor"""
    model.atualizar_status_professor(id_professor, 'rejeitado')
    model.atualizar_solicitacao_professor(id_professor, id_escola, 'rejeitado', id_admin, mensagem)
    
    # Envia email
    professor = model.buscar_professor(id_professor)
    enviar_email_rejeicao('professor', professor[3], professor[1], mensagem)


# ===== AVISOS =====

def criar_aviso(titulo, conteudo, prioridade, arquivo, id_admin, id_escola):
    """Cria novo aviso"""
    return model.inserir_aviso(titulo, conteudo, prioridade, arquivo, id_admin, id_escola)


def editar_aviso(id_aviso, titulo, conteudo, prioridade, arquivo):
    """Edita aviso existente"""
    model.atualizar_aviso(id_aviso, titulo, conteudo, prioridade, arquivo)


def deletar_aviso(id_aviso):
    """Deleta aviso (soft delete)"""
    model.deletar_aviso(id_aviso)


def listar_avisos(id_escola):
    """Lista todos os avisos da escola"""
    return model.listar_avisos_escola(id_escola)


# ===== TURMAS (Admin) =====


def criar_turma_admin(nome, descricao, especialidade, id_professor, id_escola):
    """Admin cria turma"""
    return model.inserir_turma(nome, descricao, especialidade, id_professor, id_escola, criada_por='admin')


def editar_turma(id_turma, nome, descricao, especialidade, id_professor):
    """Edita turma existente"""
    model.atualizar_turma(id_turma, nome, descricao, especialidade, id_professor)


def deletar_turma(id_turma):
    """Deleta turma"""
    model.deletar_turma(id_turma)


def listar_professores_aprovados(id_escola):
    """Lista professores aprovados para dropdown"""
    return model.listar_professores_aprovados(id_escola)


# ===== EMAIL =====
# As funções de envio de email são simuladas com prints, mas podem ser implementadas usando SMTP ou serviços como SendGrid.
# ainda não sei se prossigo implementar o envio real de email, mas deixei a estrutura pronta para isso.

def enviar_email_aprovacao(tipo_usuario, email, nome):
    """Envia email de aprovação"""
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
    else:  # professor
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
    """Envia email de rejeição"""
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
    else:  # professor
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