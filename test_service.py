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

        mock_listar.return_value = ("Professor João", ["Aluno 1"])
        mock_nome.return_value = "Turma B"

        session = {"aluno_id": 1}

        resultado = service.buscar_pessoas_da_turma(1, session)

        assert resultado["origem"] == "aluno"

@patch("service.model.listar_materiais")
def test_sem_materiais(mock_materiais):

    mock_materiais.return_value = []

    materiais = service.buscar_dados_turmas_aluno(1, 1)

    assert materiais == {}

@patch("service.model.buscar_nome_turma")
@patch("service.model.listar_pessoas_da_turma")
def test_formato_correto_retorno(mock_listar, mock_nome):

    mock_listar.return_value = ("Prof", ["A1"])
    mock_nome.return_value = "Turma Teste"

    resultado = service.buscar_pessoas_da_turma(1, {})

    assert isinstance(resultado, dict)
    assert set(resultado.keys()) == {"nome_turma", "professor", "alunos", "origem"}