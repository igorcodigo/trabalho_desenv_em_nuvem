# Este arquivo realiza um teste automatizado da funcionalidade da API de criação de usuário.
# Ele envia uma requisição para criar um novo usuário e verifica se a resposta do servidor está correta.

import requests
import random
import string

def random_string(length=10):
    """Gera uma string aleatória de letras minúsculas."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def random_phone_number(length=10):
    """Gera uma string aleatória de dígitos."""
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))

def run_user_creation_test():
    """
    Executa um teste automatizado para o endpoint de criação de usuário.
    """
    # URL do endpoint de criação de usuários
    # Assumindo que o servidor está rodando localmente na porta 8000
    url = "http://localhost:8011/contas/api/users/"

    # Gerar dados de usuário aleatórios para evitar conflitos
    username = f"testuser_{random_string(5)}"
    password = "aVeryComplexPassword123!"
    email = f"{username}@example.com"
    phone = random_phone_number(11)
    
    # Dados para enviar na requisição POST
    payload = {
        "username": username,
        "password": password,
        "email": email,
        "full_name": "Test User",
        "phone_number": phone,
        "date_of_birth": "2000-01-01"
    }

    print(f"Tentando criar usuário: {username} com telefone: {phone}")

    try:
        # Envia a requisição POST para criar o usuário
        response = requests.post(url, json=payload)

        # Verifica se a resposta foi 201 (Created)
        assert response.status_code == 201, f"Esperado status 201, mas recebi {response.status_code}"

        data = response.json()

        # Verifica se o username retornado é o mesmo
        assert data["username"] == payload["username"], f"Username esperado '{payload['username']}', mas recebi '{data['username']}'"
        
        # Garante que o usuário foi criado no banco e tem um ID
        assert "id" in data, "A resposta não contém um 'id' para o usuário criado."

        print("✅ Teste de criação de usuário passou com sucesso!")
        print(f"   - Usuário '{data['username']}' criado com ID: {data['id']}")
        print(f"   - Nome de usuário enviado: '{payload['username']}'")
        print(f"   - Nome de usuário recebido: '{data['username']}' -> OK")

    except requests.exceptions.ConnectionError as e:
        print(f"❌ Teste falhou: Não foi possível conectar ao servidor em {url}.")
        print("   - Por favor, verifique se o servidor Django está rodando.")
    except AssertionError as e:
        print(f"❌ Teste falhou: {e}")
        if 'response' in locals():
            print(f"   - Resposta da API: {response.text}")

if __name__ == "__main__":
    run_user_creation_test()
