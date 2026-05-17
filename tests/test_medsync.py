import os
import pytest
from src.medisync import adicionar_medicamento, carregar_dados, DB_FILE
from unittest.mock import patch

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

@patch('requests.get')
def test_buscar_endereco_por_cep_sucesso(mock_get):
    # Simulando que a API do ViaCEP respondeu com sucesso (Status 200) e dados válidos
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP"
    }
    
    from src.medisync import buscar_endereco_por_cep
    resultado = buscar_endereco_por_cep("01001000")
    
    assert resultado == "Praça da Sé, Sé - São Paulo/SP"

@patch('requests.get')
def test_buscar_endereco_por_cep_falha(mock_get):
    # Simulando que a API falhou (Status 404 ou erro de conexão)
    mock_get.return_value.status_code = 404
    
    from src.medisync import buscar_endereco_por_cep
    resultado = buscar_endereco_por_cep("99999999")
    
    assert resultado is None


