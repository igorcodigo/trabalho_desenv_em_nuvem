
# Como usar
## Passo 1 - Clonar este repositório

Use um dos seguintes comandos no terminal para clonar os arquivos.

- Para clonar na pasta atual:
  ```sh
  git clone https://github.com/igorcodigo/trabalho_desenv_em_nuvem .
  ```

- Para clonar em uma nova subpasta:
  ```sh
  git clone https://github.com/igorcodigo/trabalho_desenv_em_nuvem.git
  ```

## Passo 2 - Ligar o servidor

Você pode ligar o servidor de duas maneiras:

<details>
<summary><strong>Opção 1: Usando o script de inicialização (Recomendado)</strong></summary>

Se você tem Python instalado, esta é a maneira mais fácil. O script detecta seu sistema operacional e configura o ambiente apropriado.

Execute o seguinte comando na raiz do projeto:

```sh
python initialize.py
```

</details>

<details>
<summary><strong>Opção 2: Manualmente com Docker Compose (se não tiver Python)</strong></summary>

Se você não tem Python, pode usar os comandos do Docker Compose diretamente.

1.  **Navegue até a raiz do projeto.**

2.  **Pare e remova containers existentes (se houver):**
    ```sh
    docker compose -f docker/docker-compose.yml down
    ```

3.  **Inicie os serviços com base no seu ambiente:**

    -   **Para Desenvolvimento (Windows/Mac):**
        ```sh
        docker compose -f docker/docker-compose.yml --profile development up --build -d
        ```
</details>


## Testes Automatizados

Este projeto inclui scripts para testes automatizados de funcionalidades específicas da API.

### Funcionalidade: Teste de Criação de Usuário

O arquivo `teste_automatizado.py` na raiz do projeto contém um teste para a funcionalidade de criação de usuário. Ele envia uma requisição para o endpoint `POST /contas/api/users/` e valida se a resposta está correta, garantindo que o usuário foi criado como esperado.

**Como executar:**

1.  Certifique-se de que o ambiente de desenvolvimento esteja rodando.
2.  Execute o script de teste com o seguinte comando:
    ```bash
    python teste_automatizado.py
    ```



## Documentação da API

### Autenticação (JWT)

#### `POST /contas/api/token/`
- **Descrição**: Autenticação de usuário e obtenção de tokens JWT.
- **Request Body**:
  ```json
  {
    "login": "seu_username_ou_email",
    "password": "sua_senha"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### `POST /contas/api/token/refresh/`
- **Descrição**: Renova o token de acesso usando o token de refresh.
- **Request Body**:
  ```json
  {
    "refresh": "seu_refresh_token"
  }
  ```
- **Response (Success)**:
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

#### `POST /contas/api/token/logout/`
- **Descrição**: Realiza o logout do usuário invalidando o token de refresh.
- **Headers**:
  - `Authorization: Bearer <seu_token_de_acesso>`
- **Request Body**:
  ```json
  {
    "refresh": "seu_refresh_token"
  }
  ```
- **Response (Success)**: `204 No Content`

### Usuários

O CRUD de usuários é gerenciado pelo `UserViewSet`.

#### `GET /contas/api/users/`
- **Descrição**: Lista todos os usuários.
- **Acesso**: Requer autenticação.

#### `POST /contas/api/users/`
- **Descrição**: Cria um novo usuário.
- **Request Body**:
  ```json
  {
    "username": "novo_usuario",
    "password": "senha_forte",
    "email": "email@exemplo.com",
    "phone_number": "(opcional)",
    "full_name": "Nome Completo (opcional)",
    "date_of_birth": "YYYY-MM-DD (opcional)"
  }
  ```

#### `GET /contas/api/users/{id}/`
- **Descrição**: Obtém os detalhes de um usuário específico.
- **Acesso**: Requer autenticação.

#### `PUT /contas/api/users/{id}/`
- **Descrição**: Atualiza completamente um usuário.
- **Acesso**: Requer autenticação.
- **Request Body**:
  ```json
  {
    "username": "usuario_atualizado",
    "email": "email_atualizado@exemplo.com",
    ...
  }
  ```

#### `PATCH /contas/api/users/{id}/`
- **Descrição**: Atualiza parcialmente um usuário.
- **Acesso**: Requer autenticação.

#### `DELETE /contas/api/users/{id}/`
- **Descrição**: Deleta um usuário.
- **Acesso**: Requer autenticação.

#### `GET /contas/api/me/`
- **Descrição**: Retorna os dados do usuário autenticado.
- **Headers**:
  - `Authorization: Bearer <seu_token_de_acesso>`
- **Acesso**: Requer autenticação.

