from flask import Flask, render_template, request, redirect, flash, session
import model
import os
import service

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.secret_key = "WOAAHH"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrar.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/conexao_escola")
def conexao_escola():

    escolas = model.listar_escolas()

    return render_template(
        "conexao_escola.html",
        escolas=escolas
    )

@app.route("/professor", methods=["GET", "POST"])
def professor():
    if "professor_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        id_turma = int(request.form["id_turma"])
        arquivo = request.files["arquivo"]

        if arquivo and arquivo.filename != "":
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(caminho)
        else:
            caminho = None

        from datetime import datetime
        data_envio = datetime.now().strftime("%Y-%m-%d")

        id_professor = session["professor_id"]

        model.publicar_material(
            titulo,
            descricao,
            caminho,  
            data_envio,
            id_turma,
            id_professor
        )

        return redirect("/professor")  

    id_professor = session["professor_id"]
    id_escola = session["id_escola"]

    escola = model.buscar_escola(id_escola)
    turmas = model.listar_turmas_do_professor(id_professor)
    materiais = model.listar_materiais_professor(id_professor)

    materiais_por_turma = {}

    for m in materiais:
        id_turma = m[3]

        if id_turma not in materiais_por_turma:
            materiais_por_turma[id_turma] = []

        materiais_por_turma[id_turma].append(m)

    return render_template(
        "professor.html",
        escola=escola,
        turmas=turmas,
        materiais_por_turma=materiais_por_turma
    )

@app.route("/escola")
def escola():

    if "aluno_id" not in session:
        return redirect("/")

    id_escola = session["id_escola"]

    escola = model.buscar_escola(id_escola)
    avisos = model.listar_avisos_escola(id_escola)

    return render_template("escola.html", escola=escola, avisos=avisos)


@app.route("/turmas")
def turmas():

    if "aluno_id" not in session:
        return redirect("/")

    id_aluno = session["aluno_id"]
    id_escola = session["id_escola"]
   
    turmas, escola, materiais_por_turma = service.buscar_dados_turmas_aluno(id_aluno, id_escola)

    return render_template(
        "turmas.html",
        turmas=turmas,
        escola=escola,
        materiais_por_turma=materiais_por_turma
    )


@app.route("/turma/<int:id_turma>/pessoas")
def turma_pessoas(id_turma):

    dados = service.buscar_pessoas_da_turma(id_turma, session)

    if dados is None:
        return None

    return render_template(
        "turma_pessoas.html",
        nome_turma=dados["nome_turma"],
        professor=dados["professor"],
        alunos=dados["alunos"],
        origem=dados["origem"]
    )
    

@app.route("/fazer_login_aluno", methods=["POST"])
def fazer_login_aluno():
    email = request.form["email"]
    senha = request.form["senha"]
    
    aluno = model.aluno_login(email, senha)
    
    if not aluno:
        flash("Email ou senha inválidos.")
        return redirect("/login")
    
    # Verifica status_escola
    if aluno[7] == 'pendente':  # status_escola é a coluna 7
        flash("Sua solicitação está em análise. Aguarde aprovação do administrador.")
        return redirect("/login")
    
    if aluno[7] == 'rejeitado':  # status_escola
        flash("Sua solicitação foi rejeitada. Entre em contato com a escola.")
        return redirect("/login")
    
    # Se aprovado, continua o fluxo normal
    resultado = service.fazer_login_aluno(email, senha)
    
    if resultado["sucesso"]:
        session["aluno_id"] = resultado["aluno_id"]
        session["id_escola"] = resultado["id_escola"]
        return redirect("/escola")
    
    flash(resultado["mensagem"])
    return redirect("/login")


@app.route("/fazer_login_professor", methods=["POST"])
def fazer_login_professor():
    email = request.form["email"]
    senha = request.form["senha"]
    
    resultado = service.fazer_login_professor(email, senha)
    
    if resultado["sucesso"]:
        session["professor_id"] = resultado["professor_id"]
        session["id_escola"] = resultado["id_escola"]
        return redirect("/professor")
    
    flash(resultado["mensagem"])
    return redirect("/login")


@app.route("/cadastrar_aluno", methods=["POST"])
def cadastrar_aluno():
    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    endereco = request.form["endereco"]
    senha = request.form["senha"]

    cadastro = model.cadastro_aluno(nome, email, endereco, telefone, senha, None)

    if cadastro:
        # Pega o ID do aluno recém criado
        aluno = model.aluno_login(email, senha)
        if aluno:
            # Cria solicitação pendente
            model.inserir_solicitacao_aluno(aluno[0], None)
        
        flash("Sua solicitação foi enviada! Aguarde aprovação do administrador da escola.")
        return redirect("/login")
    else:
        flash("Email já cadastrado.")
        return redirect("/cadastrar")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

# ===== ROTAS DO ADMIN =====

@app.route("/admin/login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/fazer_login_admin", methods=["POST"])
def fazer_login_admin():
    email = request.form["email"]
    senha = request.form["senha"]
    
    resultado = service.fazer_login_admin(email, senha)
    
    if resultado["sucesso"]:
        session["admin_id"] = resultado["admin_id"]
        session["id_escola"] = resultado["id_escola"]
        return redirect("/admin/dashboard")
    
    flash(resultado["mensagem"])
    return redirect("/admin/login")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    
    stats = service.buscar_dashboard_admin(id_escola)
    
    return render_template(
        "admin_dashboard.html",
        stats=stats
    )


# ===== SOLICITAÇÕES ALUNOS =====

@app.route("/admin/solicitacoes/alunos")
def admin_solicitacoes_alunos():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    solicitacoes_pendentes = service.listar_solicitacoes_alunos(id_escola, 'pendente')
    solicitacoes_aprovadas = service.listar_solicitacoes_alunos(id_escola, 'aprovado')
    
    return render_template(
        "admin_solicitacoes_alunos.html",
        pendentes=solicitacoes_pendentes,
        aprovados=solicitacoes_aprovadas
    )


@app.route("/admin/alunos/rejeitados")
def admin_alunos_rejeitados():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    solicitacoes_rejeitadas = service.listar_solicitacoes_alunos(id_escola, 'rejeitado')
    
    return render_template(
        "admin_alunos_rejeitados.html",
        rejeitados=solicitacoes_rejeitadas
    )


@app.route("/admin/aluno/<int:id_aluno>/revisar")
def admin_revisar_aluno(id_aluno):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    dados = service.revisar_aluno(id_aluno, id_escola)
    
    return render_template(
        "admin_aluno_revisar.html",
        aluno=dados["aluno"],
        solicitacao=dados["solicitacao"]
    )


@app.route("/admin/aluno/<int:id_aluno>/aprovar", methods=["POST"])
def admin_aprovar_aluno(id_aluno):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_admin = session["admin_id"]
    id_escola = session["id_escola"]
    
    service.aprovar_aluno(id_aluno, id_escola, id_admin)
    
    flash("Aluno aprovado com sucesso!")
    return redirect("/admin/solicitacoes/alunos")


@app.route("/admin/aluno/<int:id_aluno>/rejeitar", methods=["POST"])
def admin_rejeitar_aluno(id_aluno):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_admin = session["admin_id"]
    id_escola = session["id_escola"]
    mensagem = request.form.get("mensagem", "")
    
    service.rejeitar_aluno(id_aluno, id_escola, id_admin, mensagem)
    
    flash("Aluno rejeitado!")
    return redirect("/admin/solicitacoes/alunos")


# ===== SOLICITAÇÕES PROFESSORES =====

@app.route("/admin/solicitacoes/professores")
def admin_solicitacoes_professores():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    solicitacoes_pendentes = service.listar_solicitacoes_professores(id_escola, 'pendente')
    solicitacoes_aprovadas = service.listar_solicitacoes_professores(id_escola, 'aprovado')
    
    return render_template(
        "admin_solicitacoes_professores.html",
        pendentes=solicitacoes_pendentes,
        aprovados=solicitacoes_aprovadas
    )


@app.route("/admin/professor/<int:id_professor>/revisar")
def admin_revisar_professor(id_professor):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    dados = service.revisar_professor(id_professor, id_escola)
    
    return render_template(
        "admin_professor_revisar.html",
        professor=dados["professor"],
        solicitacao=dados["solicitacao"]
    )


@app.route("/admin/professor/<int:id_professor>/aprovar", methods=["POST"])
def admin_aprovar_professor(id_professor):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_admin = session["admin_id"]
    id_escola = session["id_escola"]
    
    service.aprovar_professor(id_professor, id_escola, id_admin)
    
    flash("Professor aprovado com sucesso!")
    return redirect("/admin/solicitacoes/professores")


@app.route("/admin/professor/<int:id_professor>/rejeitar", methods=["POST"])
def admin_rejeitar_professor(id_professor):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_admin = session["admin_id"]
    id_escola = session["id_escola"]
    mensagem = request.form.get("mensagem", "")
    
    service.rejeitar_professor(id_professor, id_escola, id_admin, mensagem)
    
    flash("Professor rejeitado!")
    return redirect("/admin/solicitacoes/professores")


# ===== AVISOS =====

@app.route("/admin/avisos")
def admin_avisos():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    avisos = service.listar_avisos(id_escola)
    
    return render_template(
        "admin_avisos.html",
        avisos=avisos
    )


@app.route("/admin/avisos/novo", methods=["GET", "POST"])
def admin_aviso_novo():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        conteudo = request.form["conteudo"]
        prioridade = request.form.get("prioridade", "normal")
        arquivo = request.files.get("arquivo")
        
        id_admin = session["admin_id"]
        id_escola = session["id_escola"]
        
        caminho_arquivo = None
        if arquivo and arquivo.filename != "":
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], "avisos", arquivo.filename)
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            arquivo.save(caminho)
            caminho_arquivo = caminho
        
        service.criar_aviso(titulo, conteudo, prioridade, caminho_arquivo, id_admin, id_escola)
        
        flash("Aviso publicado com sucesso!")
        return redirect("/admin/avisos")
    
    return render_template("admin_aviso_novo.html")


@app.route("/admin/avisos/<int:id_aviso>/editar", methods=["GET", "POST"])
def admin_aviso_editar(id_aviso):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    aviso = model.buscar_aviso(id_aviso)
    
    if not aviso:
        flash("Aviso não encontrado!")
        return redirect("/admin/avisos")
    
    if request.method == "POST":
        titulo = request.form.get("titulo", "")
        conteudo = request.form["conteudo"]
        prioridade = request.form.get("prioridade", "normal")
        arquivo = request.files.get("arquivo")
        
        caminho_arquivo = aviso[4]  
        
        if arquivo and arquivo.filename != "":
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], "avisos", arquivo.filename)
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            arquivo.save(caminho)
            caminho_arquivo = caminho
        
        service.editar_aviso(id_aviso, titulo, conteudo, prioridade, caminho_arquivo)
        
        flash("Aviso atualizado com sucesso!")
        return redirect("/admin/avisos")
    
    return render_template(
        "admin_aviso_editar.html",
        aviso=aviso
    )


@app.route("/admin/avisos/<int:id_aviso>/deletar", methods=["POST"])
def admin_deletar_aviso(id_aviso):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    service.deletar_aviso(id_aviso)
    
    flash("Aviso deletado!")
    return redirect("/admin/avisos")


# ===== TURMAS (ADMIN) =====

@app.route("/admin/turmas")
def admin_turmas():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    
    turmas = model.listar_turmas_por_escola(id_escola)
    
    return render_template(
        "admin_turmas.html",
        turmas=turmas
    )


@app.route("/admin/turmas/nova", methods=["GET", "POST"])
def admin_turma_nova():
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    professores = service.listar_professores_aprovados(id_escola)
    
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        especialidade = request.form["especialidade"]
        id_professor = request.form["id_professor"]
        
        service.criar_turma_admin(nome, descricao, especialidade, int(id_professor), id_escola)
        
        flash("Turma criada com sucesso!")
        return redirect("/admin/turmas")
    
    return render_template(
        "admin_turma_nova.html",
        professores=professores
    )


@app.route("/admin/turmas/<int:id_turma>/editar", methods=["GET", "POST"])
def admin_turma_editar(id_turma):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    id_escola = session["id_escola"]
    turma = model.buscar_turma(id_turma)
    professores = service.listar_professores_aprovados(id_escola)
    
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        especialidade = request.form["especialidade"]
        id_professor = request.form["id_professor"]
        
        service.editar_turma(id_turma, nome, descricao, especialidade, int(id_professor))
        
        flash("Turma atualizada!")
        return redirect("/admin/turmas")
    
    return render_template(
        "admin_turma_editar.html",
        turma=turma,
        professores=professores
    )


@app.route("/admin/turmas/<int:id_turma>/deletar", methods=["POST"])
def admin_deletar_turma(id_turma):
    if "admin_id" not in session:
        return redirect("/admin/login")
    
    service.deletar_turma(id_turma)
    
    flash("Turma deletada!")
    return redirect("/admin/turmas")

if __name__ == "__main__":
    app.run(debug=True)