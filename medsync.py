import json
import os

DB_FILE = "medicamentos.json"
__version__ = "1.0.0" # Versionamento Semântico

def carregar_dados():
    """Carrega os dados do arquivo JSON. Se não existir, retorna lista vazia."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    """Salva a lista de medicamentos no arquivo JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def adicionar_medicamento(nome, horario, especificacao):
    """Regra de Negócio: Adiciona um medicamento se os dados forem válidos."""
    if not nome or not horario:
        return False, "Erro: Nome e horário são obrigatórios."
    
    dados = carregar_dados()
    dados.append({"nome": nome, "horario": horario, "especificacao": especificacao})
    salvar_dados(dados)
    return True, "Medicamento adicionado com sucesso!"

def menu():
    """Interface CLI do usuário."""
    while True:
        print(f"\n--- MediSync v{__version__} ---")
        print("1. Adicionar Medicamento")
        print("2. Listar Medicamentos")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do medicamento: ")
            horario = input("Horário (ex: 08:00): ")
            especificacao = input("Especificação (ex: 50mg): ")
            sucesso, msg = adicionar_medicamento(nome, horario, especificacao)
            print(msg)
        elif escolha == '2':
            meds = carregar_dados()
            if not meds:
                print("Nenhum medicamento cadastrado.")
            else:
                print("\n--- Seus Medicamentos ---")
                for i, m in enumerate(meds, 1):
                    print(f"{i}. {m['nome']} | Horário: {m['horario']} | Uso: {m['especificacao']}")
        elif escolha == '3':
            print("Saindo... Lembre-se de tomar sua água e seus remédios!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()