
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

    -   **Para Staging/Produção (Linux):**
        O ambiente em Linux (`staging` ou `production`) é determinado pelo endereço IP do servidor, conforme configurado no arquivo `.env`. Para execução manual, escolha um dos perfis abaixo.

        -   **Ambiente de Staging:**
            ```sh
            docker compose -f docker/docker-compose.yml --profile staging up --build -d
            ```

        -   **Ambiente de Produção:**
            ```sh
            docker compose -f docker/docker-compose.yml --profile production up --build -d
            ```
</details>

## Endpoints Disponíveis
#### `/admin/`
- **Descrição**: Interface de administração do Django.
- **Acesso**: Apenas administradores autenticados.

#### `/contas/login/`
- **Descrição**: Página de login para autenticação via interface web.

