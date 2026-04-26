from flask import Flask, render_template, request, redirect, flash, session
import model
import os
import service

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.secret_key = os.environ.get("SECRET_KEY", " when candles burn out and the record is faded down I know you've got people to turn to")


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
    return render_template("conexao_escola.html", escolas=escolas)


@app.route("/professor", methods=["GET", "POST"])
def professor():
    if "professor_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        id_turma = request.form["id_turma"]
        id_professor = session["professor_id"]
        arquivo = request.files.get("arquivo")

        caminho_arquivo = None
        if arquivo and arquivo.filename != "":
            caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
            arquivo.save(caminho)
            caminho_arquivo = caminho

        resultado = service.publicar_material_professor(
            titulo, descricao, caminho_arquivo, id_turma, id_professor
        )

        if not resultado["sucesso"]:
            flash(resultado["mensagem"])

        return redirect("/professor")

    id_professor = session["professor_id"]
    id_escola = session["id_escola"]

    escola = model.buscar_escola(id_escola)
    turmas = model.listar_turmas_do_professor(id_professor)
    materiais = model.listar_materiais_professor(id_professor)
    avisos = model.listar_avisos_escola(id_escola)

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
        materiais_por_turma=materiais_por_turma,
        avisos=avisos
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

    if aluno[7] == 'pendente':
        flash("Sua solicitação está em análise. Aguarde aprovação do administrador.")
        return redirect("/login")

    if aluno[7] == 'rejeitado':
        flash("Sua solicitação foi rejeitada. Entre em contato com a escola.")
        return redirect("/login")

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
        aluno = model.aluno_login(email, senha)
        if aluno:
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
    return render_template("login.html")


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

    return render_template("dashboard_admin.html", stats=stats)


# ===== SOLICITAÇÕES ALUNOS E PROFESSORES =====

@app.route("/admin/solicitacoes")
def admin_solicitacoes():
    if "admin_id" not in session:
        return redirect("/admin/login")

    id_escola = session["id_escola"]

    alunos_pendentes  = service.listar_solicitacoes_alunos(id_escola, 'pendente')
    alunos_aprovados  = service.listar_solicitacoes_alunos(id_escola, 'aprovado')
    alunos_rejeitados = service.listar_solicitacoes_alunos(id_escola, 'rejeitado')

    profs_pendentes  = service.listar_solicitacoes_professores(id_escola, 'pendente')
    profs_aprovados  = service.listar_solicitacoes_professores(id_escola, 'aprovado')
    profs_rejeitados = service.listar_solicitacoes_professores(id_escola, 'rejeitado')

    return render_template(
        "solicitacoes_admin.html",
        alunos_pendentes=alunos_pendentes,
        alunos_aprovados=alunos_aprovados,
        alunos_rejeitados=alunos_rejeitados,
        profs_pendentes=profs_pendentes,
        profs_aprovados=profs_aprovados,
        profs_rejeitados=profs_rejeitados
    )


@app.route("/admin/aluno/<int:id_aluno>/aprovar", methods=["POST"])
def admin_aprovar_aluno(id_aluno):
    if "admin_id" not in session:
        return redirect("/admin/login")

    service.aprovar_aluno(id_aluno, session["id_escola"], session["admin_id"])
    flash("Aluno aprovado com sucesso!")
    return redirect("/admin/solicitacoes")


@app.route("/admin/aluno/<int:id_aluno>/rejeitar", methods=["POST"])
def admin_rejeitar_aluno(id_aluno):
    if "admin_id" not in session:
        return redirect("/admin/login")

    mensagem = request.form.get("mensagem", "")
    service.rejeitar_aluno(id_aluno, session["id_escola"], session["admin_id"], mensagem)
    flash("Aluno rejeitado!")
    return redirect("/admin/solicitacoes")


@app.route("/admin/professor/<int:id_professor>/aprovar", methods=["POST"])
def admin_aprovar_professor(id_professor):
    if "admin_id" not in session:
        return redirect("/admin/login")

    service.aprovar_professor(id_professor, session["id_escola"], session["admin_id"])
    flash("Professor aprovado com sucesso!")
    return redirect("/admin/solicitacoes")


@app.route("/admin/professor/<int:id_professor>/rejeitar", methods=["POST"])
def admin_rejeitar_professor(id_professor):
    if "admin_id" not in session:
        return redirect("/admin/login")

    mensagem = request.form.get("mensagem", "")
    service.rejeitar_professor(id_professor, session["id_escola"], session["admin_id"], mensagem)
    flash("Professor rejeitado!")
    return redirect("/admin/solicitacoes")


# ===== AVISOS =====

@app.route("/admin/avisos")
def admin_avisos():
    if "admin_id" not in session:
        return redirect("/admin/login")

    avisos = service.listar_avisos(session["id_escola"])
    return render_template("avisos_admin.html", avisos=avisos)


@app.route("/admin/avisos/novo", methods=["POST"])
def admin_aviso_novo():
    if "admin_id" not in session:
        return redirect("/admin/login")

    titulo    = request.form.get("titulo", "")
    conteudo  = request.form["conteudo"]
    prioridade = request.form.get("prioridade", "normal")
    arquivo   = request.files.get("arquivo")

    caminho_arquivo = None
    if arquivo and arquivo.filename != "":
        caminho = os.path.join(app.config["UPLOAD_FOLDER"], "avisos", arquivo.filename)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        arquivo.save(caminho)
        caminho_arquivo = caminho

    service.criar_aviso(titulo, conteudo, prioridade, caminho_arquivo, session["admin_id"], session["id_escola"])
    flash("Aviso publicado com sucesso!")
    return redirect("/admin/avisos")

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
    professores = service.listar_professores_aprovados(id_escola)

    return render_template("turmas_admin.html", turmas=turmas, professores=professores) 


@app.route("/admin/turmas/<int:id_turma>/deletar", methods=["POST"])
def admin_deletar_turma(id_turma):
    if "admin_id" not in session:
        return redirect("/admin/login")

    service.deletar_turma(id_turma)
    flash("Turma deletada!")
    return redirect("/admin/turmas")


if __name__ == "__main__":
    app.run(debug=True)