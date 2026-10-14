# Sistema de Registro de Biblioteca

Projeto pessoal de estudo: um sistema web simples para gerenciar uma biblioteca, com interface em **HTML, CSS e JavaScript**, API em **Python com FastAPI** e banco de dados **MongoDB**.

O objetivo é aprender, na prática, como a interface, a API e o banco de dados se conectam.

> **Status:** funcionalidades principais implementadas para cadastrar e consultar livros e usuários, além de registrar empréstimos e devoluções. O projeto continua sendo uma versão de estudo.

## Como o sistema funciona

O sistema tem três partes:

```text
Interface web  →  API  →  MongoDB
```

- **Front-end:** mostra as telas e envia requisições HTTP à API usando JavaScript e `fetch`. Não acessa o banco diretamente.
- **API:** recebe as requisições, valida os dados, aplica as regras do sistema e acessa o banco.
- **MongoDB:** armazena livros, usuários e empréstimos.

## Tecnologias

- **Python**, com FastAPI, Uvicorn, Pydantic e PyMongo
- **MongoDB**, executado localmente e visualizado pelo MongoDB Compass
- **HTML, CSS e JavaScript** para a interface web
- **Git e GitHub** para versionamento
- **Live Server** do VS Code para abrir a interface
- **Postman** e a documentação `/docs` do FastAPI para consultar e testar a API

## Estrutura do projeto

```text
APIBIBLIOTECA/
├── backend/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── emprestimos.py
│   │   ├── livros.py
│   │   └── usuarios.py
│   ├── database.py
│   ├── main.py
│   ├── requirements.txt
│   ├── schemas.py
│   └── utils.py
├── frontend/
│   ├── index.html
│   └── style.css
├── .gitignore
└── README.md
```

## Modelo de dados

O banco se chama `biblioteca` e possui três coleções:

| Coleção | Campos principais |
|---|---|
| `livros` | `titulo`, `autor`, `ano`, `exemplares`, `disponivel` |
| `usuarios` | `nome`, `email`, `data_cadastro` |
| `emprestimos` | `livro_id`, `usuario_id`, `data_emprestimo`, `data_prevista_devolucao`, `data_devolucao` |

Cada documento recebe um `_id` gerado pelo MongoDB. Um empréstimo guarda os IDs do livro e do usuário associados a ele. A interface usa esses IDs para encontrar e mostrar os nomes correspondentes.

## Rotas da API

| Método | Rota | O que faz |
|---|---|---|
| GET | `/` | Confirma que a API está funcionando |
| GET | `/livros` | Lista os livros |
| POST | `/livros` | Cadastra um livro |
| GET | `/livros/{livro_id}` | Busca um livro pelo ID |
| PATCH | `/livros/{livro_id}` | Atualiza os dados de um livro |
| DELETE | `/livros/{livro_id}` | Exclui um livro que não tenha empréstimos registrados |
| GET | `/usuarios` | Lista os usuários |
| POST | `/usuarios` | Cadastra um usuário |
| GET | `/emprestimos` | Lista os empréstimos |
| POST | `/emprestimos` | Registra um empréstimo |
| PATCH | `/emprestimos/{emprestimo_id}/devolucao` | Registra a devolução de um empréstimo |

Com a API em execução, a documentação interativa do FastAPI fica em `http://127.0.0.1:8000/docs`.

## Regras do sistema

- Título e autor do livro são obrigatórios; o ano deve ser numérico e a quantidade de exemplares não pode ser negativa.
- Um livro com zero exemplares fica indisponível (`disponivel: false`).
- O cadastro normaliza o e-mail do usuário, removendo espaços nas pontas e convertendo-o para minúsculas, e verifica se já existe outro cadastro com esse e-mail.
- Um empréstimo exige um livro existente, um usuário existente e pelo menos um exemplar disponível.
- Cada empréstimo tem prazo previsto de 14 dias e reduz em um a quantidade disponível do livro.
- A atualização condicional do estoque impede que dois empréstimos simultâneos retirem o mesmo último exemplar.
- Cada empréstimo só pode ser devolvido uma vez; a devolução repõe um exemplar ao estoque.
- Um livro com empréstimos registrados não pode ser excluído, para preservar o histórico.

## Como rodar o projeto

### Pré-requisitos

- Python 3.10 ou mais novo
- MongoDB Community Server em execução em `localhost:27017`
- Git
- VS Code com a extensão Live Server

### Iniciar a API no Windows / PowerShell

1. Clone o repositório e entre na pasta `backend`:

   ```powershell
   git clone https://github.com/akemiartxDEV/livrariaAPIMongoDB-projetopessoal.git
   cd livrariaAPIMongoDB-projetopessoal/backend
   ```

2. Crie e ative o ambiente virtual:

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   Se o PowerShell bloquear a execução de scripts, ajuste a política para o seu usuário:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

3. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

4. Inicie a API:

   ```powershell
   uvicorn main:app --reload
   ```

5. Para abrir a documentação da API, acesse `http://127.0.0.1:8000/docs`.

### Abrir o front-end

Com o MongoDB e a API em execução, abra `frontend/index.html` com o Live Server do VS Code. O Live Server deve usar a porta `5500`, permitida pela configuração de CORS da API.

O banco `biblioteca` e as coleções são criados pelo MongoDB quando os primeiros documentos são gravados.

## Progresso

- [x] Ambiente Python e dependências configurados
- [x] Conexão com o MongoDB
- [x] API com FastAPI e rotas organizadas
- [x] Cadastro, listagem, consulta, atualização e exclusão protegida de livros
- [x] Cadastro e listagem de usuários
- [x] Registro e listagem de empréstimos
- [x] Registro de devoluções e controle de exemplares
- [x] Interface web para livros, usuários e empréstimos
- [x] Estilização da interface

## Segurança e limitações

Este é um projeto de estudo local e não possui login nem controle de permissões. Ele não deve ser exposto à internet como sistema de produção.

Atualmente, a conexão com o MongoDB usa o endereço local `mongodb://localhost:27017`, definido no código. O `.gitignore` ignora arquivos `.env`; para usar um banco na nuvem, seria necessário guardar a URI em uma variável de ambiente e adaptar o código para lê-la. Credenciais não devem ser enviadas ao GitHub.

As alterações de estoque e os registros de empréstimo usam mais de uma operação no banco. Para um sistema de produção, seria necessário avaliar transações, backups, autenticação e outras medidas de segurança.

## Autoria

Projeto pessoal de estudo, desenvolvido passo a passo para aprender e documentar a construção de uma API e sua interface.