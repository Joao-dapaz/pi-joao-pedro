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

    return render_template("escola.html", escola=escola)


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
        return redirect("/conexao_escola")
    else:
        flash("Email já cadastrado.")
        return redirect("/cadastrar")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)