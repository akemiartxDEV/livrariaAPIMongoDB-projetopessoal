# Sistema de Registro de Biblioteca

Projeto pessoal de estudo: um sistema simples de biblioteca, com **API em Python**, banco de dados **MongoDB** e, futuramente, uma **interface web** funcional.

O objetivo é aprender, na prática, como as partes de um sistema real se conectam: banco de dados, API e front end.

> **Status:** em desenvolvimento. O ambiente está configurado e o Python já conversa com o MongoDB. A API e o front end ainda serão construídos.

---

## Como o sistema funciona

O projeto é dividido em três camadas:

```
Front end (HTML + JavaScript)  →  API (Python)  →  MongoDB
```

- **Front end:** as telas que o usuário vê e usa. Nunca conversa direto com o banco.
- **API:** intermediária entre o front end e o banco. Recebe os pedidos, aplica as regras do sistema e acessa os dados.
- **MongoDB:** guarda os dados de forma permanente.

## Tecnologias

- **Python** (com [FastAPI](https://fastapi.tiangolo.com/), Uvicorn e PyMongo)
- **MongoDB** (rodando localmente, visualizado pelo MongoDB Compass)
- **JavaScript, HTML e CSS** (front end, ainda a fazer)
- **Git e GitHub** para versionamento
- **Postman** para testar a API

## Estrutura do projeto

```
APIBIBLIOTECA/
├── backend/        # API em Python
├── frontend/       # Interface web (a fazer)
├── docs/           # Documentação do projeto (a fazer)
├── .gitignore
└── README.md
```

## Modelo de dados (planejado)

O banco se chama `biblioteca` e terá três coleções:

| Coleção       | O que guarda                                                                 |
|---------------|------------------------------------------------------------------------------|
| `livros`      | título, autor, ano, exemplares, disponível                                   |
| `usuarios`    | nome, e-mail, data de cadastro                                               |
| `emprestimos` | livro, usuário, data do empréstimo, data prevista e data de devolução        |

Por enquanto, apenas a coleção `livros` foi criada, por meio do script `primeiro_livro.py`.

## Como rodar o projeto

### Pré-requisitos

- [Python](https://www.python.org/downloads/) 3.10 ou mais novo
- [MongoDB Community Server](https://www.mongodb.com/try/download/community) rodando em `localhost:27017`
- [Git](https://git-scm.com/)

### Passo a passo (Windows / PowerShell)

1. Clonar o repositório:
   ```
   git clone https://github.com/akemiartxDEV/libraryAPIMongoDB-personalproject.git
   cd libraryAPIMongoDB-personalproject/backend
   ```

2. Criar e ativar o ambiente virtual:
   ```
   py -m venv venv
   venv\Scripts\Activate.ps1
   ```
   Se o PowerShell bloquear a execução de scripts, rode uma vez:
   ```
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

3. Instalar as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Testar a conexão com o MongoDB:
   ```
   python teste_conexao.py
   ```
   Deve aparecer a lista de bancos existentes no seu MongoDB.

5. Guardar um livro de exemplo:
   ```
   python primeiro_livro.py
   ```
   O livro pode ser visto no MongoDB Compass, no banco `biblioteca`, coleção `livros`.

## Arquivos do backend

| Arquivo               | Para que serve                                                      |
|-----------------------|---------------------------------------------------------------------|
| `teste_conexao.py`    | Confirma que o Python consegue se conectar ao MongoDB               |
| `primeiro_livro.py`   | Guarda um livro no banco e lista os livros existentes               |
| `requirements.txt`    | Lista as bibliotecas (e versões) necessárias para rodar o projeto   |

## Progresso

- [x] Ambiente Python configurado (ambiente virtual e dependências)
- [x] Conexão entre Python e MongoDB
- [x] Primeiro livro guardado no banco por código
- [x] Projeto versionado no GitHub
- [x] API com FastAPI
- [x] Cadastro, listagem, busca, atualização e remoção de livros
- [ ] Usuários e empréstimos, com as regras de negócio
- [ ] Interface web (front end)
- [ ] Documentação da API e do modelo de dados

## Segurança

Este repositório é público. Senhas e dados de conexão sensíveis **não** devem ser enviados ao GitHub: ficam em um arquivo `.env`, que está listado no `.gitignore`.

## Autoria

Projeto pessoal de estudo, desenvolvido passo a passo com o objetivo de aprender e documentar cada etapa.
Estou fazendo uso do Claude para prosseguir com a programação da API.