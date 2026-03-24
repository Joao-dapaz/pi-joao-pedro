from flask import Flask, render_template, request, redirect, flash, session
import model

app = Flask(__name__)
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

@app.route("/professor")
def professor():

    if "professor_id" not in session:
        return redirect("/login")

    return render_template("professor.html")

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

    id_escola = session["id_escola"]

    turmas = model.listar_turmas_por_escola(id_escola)
    escola = model.buscar_escola(id_escola)

    return render_template("turmas.html", turmas=turmas, escola=escola)

@app.route("/turma/<int:id_turma>/pessoas")
def turma_pessoas(id_turma):

    professor, alunos = model.listar_pessoas_da_turma(id_turma)

    if professor is None:
        return "Turma não encontrada", 404

    nome_turma = model.buscar_nome_turma(id_turma)

    return render_template(
        "turma_pessoas.html",
        nome_turma=nome_turma,
        professor=professor,
        alunos=alunos
    )


@app.route("/fazer_login_aluno", methods=["POST"])
def fazer_login_aluno():

    email = request.form["email"]
    senha = request.form["senha"]

    aluno = model.aluno_login(email, senha)

    if aluno:
        if aluno[6] is None:
            flash("Você precisa se conectar a uma escola antes de entrar.")
            return redirect("/login")

        session["aluno_id"] = aluno[0]
        session["id_escola"] = aluno[6]

        return redirect("/escola")

    flash("Email ou senha inválidos.")
    return redirect("/login")


@app.route("/fazer_login_professor", methods=["POST"])
def fazer_login_professor():

    email = request.form["email"]
    senha = request.form["senha"]

    professor = model.professor_login(email, senha)

    if professor:
        session["professor_id"] = professor[0]
        session["id_escola"] = professor[7]

        return redirect("/professor")

    flash("Email ou senha inválidos.")
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