import os
import pytest
from src.medisync import adicionar_medicamento, carregar_dados, DB_FILE

# Fixture para limpar o arquivo JSON antes e depois de cada teste
@pytest.fixture(autouse=True)
def limpar_banco_teste():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    yield
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def test_adicionar_medicamento_caminho_feliz():
    sucesso, msg = adicionar_medicamento("Losartana", "08:00", "50mg")
    assert sucesso is True
    dados = carregar_dados()
    assert len(dados) == 1
    assert dados[0]["nome"] == "Losartana"

def test_adicionar_medicamento_entrada_invalida():
    sucesso, msg = adicionar_medicamento("", "08:00", "50mg")
    assert sucesso is False
    assert "obrigatórios" in msg

def test_carregar_dados_banco_vazio():
    dados = carregar_dados()
    assert dados == []