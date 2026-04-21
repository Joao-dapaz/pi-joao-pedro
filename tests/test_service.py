import pytest
from unittest.mock import patch
import service

class Tests:

    @patch("service.model.buscar_nome_turma")
    @patch("service.model.listar_pessoas_da_turma")
    def test_buscar_turma_retorna_dados(self, mock_listar_pessoas, mock_buscar_nome):

        mock_listar_pessoas.return_value = ("sor Dani", ["Joao", "Gabigoat"])
        mock_buscar_nome.return_value = "devn241"

        session = {"professor_id": 1}

        resultado = service.buscar_pessoas_da_turma(1, session)

        assert resultado is not None
        assert resultado["nome_turma"] == "devn241"
        assert resultado["professor"] == "sor Dani"
        assert resultado["alunos"] == ["Joao", "Gabigoat"]
        assert resultado["origem"] == "professor"


    @patch("service.model.listar_pessoas_da_turma")
    def test_buscar_pessoas_turma_inexistente(self, mock_listar):

        mock_listar.return_value = (None, [])

        session = {}

        resultado = service.buscar_pessoas_da_turma(1, session)

        assert resultado == ("Turma não encontrada", 404)

    @patch("service.model.buscar_nome_turma")
    @patch("service.model.listar_pessoas_da_turma")
    def test_origem_aluno(Self, mock_listar, mock_nome):

        mock_listar.return_value = ("Professor John", ["Aluno sigma"])
        mock_nome.return_value = "Turma aura+ego"

        session = {"aluno_id": 1}

        resultado = service.buscar_pessoas_da_turma(1, session)

        assert resultado["origem"] == "aluno"

@patch("service.model.listar_materiais")
@patch("service.model.buscar_escola")
@patch("service.model.listar_turmas_do_aluno")
def test_sem_materiais(mock_turmas, mock_escola, mock_materiais):

    mock_turmas.return_value = []
    mock_escola.return_value = ("Escola senac", "", "", "")
    mock_materiais.return_value = []

    turmas, escola, materiais = service.buscar_dados_turmas_aluno(1, 1)

    assert materiais == {}

@patch("service.model.buscar_nome_turma")
@patch("service.model.listar_pessoas_da_turma")
def test_formato_correto_retorno(mock_listar, mock_nome):

    mock_listar.return_value = ("Professor snape", ["A1"])
    mock_nome.return_value = "Turma dos bobao"

    resultado = service.buscar_pessoas_da_turma(1, {})

    assert isinstance(resultado, dict)
    assert set(resultado.keys()) == {"nome_turma", "professor", "alunos", "origem"}

@patch("service.model.aluno_login")
def test_fazer_login_aluno_sucesso(mock_aluno_login):
    mock_aluno_login.return_value = (1, "João", "email@test.com", "123", "rua", "senha", 5)
    
    resultado = service.fazer_login_aluno("email@test.com", "senha")
    
    assert resultado["sucesso"] is True
    assert resultado["aluno_id"] == 1
    assert resultado["id_escola"] == 5


@patch("service.model.aluno_login")
def test_fazer_login_aluno_invalido(mock_aluno_login):
    mock_aluno_login.return_value = None
    
    resultado = service.fazer_login_aluno("email@test.com", "senha_errada")
    
    assert resultado["sucesso"] is False
    assert resultado["mensagem"] == "Email ou senha inválidos."


@patch("service.model.aluno_login")
def test_fazer_login_aluno_sem_escola(mock_aluno_login):
    mock_aluno_login.return_value = (1, "João", "email@test.com", "123", "rua", "senha", None)
    
    resultado = service.fazer_login_aluno("email@test.com", "senha")
    
    assert resultado["sucesso"] is False
    assert resultado["mensagem"] == "Você precisa se conectar a uma escola antes de entrar."


@patch("service.model.professor_login")
def test_fazer_login_professor_sucesso(mock_professor_login):
    """Teste de login de professor bem-sucedido"""
    # professor[0] = id, professor[7] = id_escola
    mock_professor_login.return_value = (1, "Dani", "dani@test.com", "123", "rua", "senha", "foto", 5)
    
    resultado = service.fazer_login_professor("dani@test.com", "senha")
    
    assert resultado["sucesso"] is True
    assert resultado["professor_id"] == 1
    assert resultado["id_escola"] == 5


@patch("service.model.professor_login")
def test_fazer_login_professor_invalido(mock_professor_login):
    """Teste com email ou senha inválidos"""
    mock_professor_login.return_value = None
    
    resultado = service.fazer_login_professor("dani@test.com", "senha_errada")
    
    assert resultado["sucesso"] is False
    assert resultado["mensagem"] == "Email ou senha inválidos."