from unittest.mock import patch
import pytest
from service import buscar_pessoas_da_turma

@patch("model.buscar_nome_turma")
@patch("model.listar_pessoas_da_turma")
class TestBuscarPessoasDaTurma:
    def test_buscar_pessoas_retorna_dados(mock_listar_pessoas, mock_buscar_nome):
        mock_listar_pessoas.return_value = ("Professor X", ["Aluno A", "Aluno B"])
        mock_buscar_nome.return_value = "Turma 1"

        resultado = buscar_pessoas_da_turma(1, {"aluno_id": 1})

        assert resultado["nome_turma"] == "Turma 1"
        assert resultado["professor"] == "Professor X"
        assert resultado["alunos"] == ["Aluno A", "Aluno B"]
        assert resultado["origem"] == "aluno"
