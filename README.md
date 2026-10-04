# Sistema de Registro de Biblioteca

Projeto pessoal de estudo: um sistema simples de biblioteca, com **API em Python**, banco de dados **MongoDB** e, em breve, uma **interface web** funcional.

O objetivo é aprender, na prática, como as partes de um sistema real se conectam: banco de dados, API e front end.

> **Status:** em desenvolvimento. A API está funcionando (livros, usuários, empréstimos e devoluções). O front end ainda será construído.

---

## Como o sistema funciona

O projeto é dividido em três camadas:

```
Front end (HTML + JavaScript)  →  API (Python)  →  MongoDB
```

- **Front end:** as telas que o usuário vê e usa. Nunca conversa direto com o banco. *(a fazer)*
- **API:** intermediária entre o front end e o banco. Recebe os pedidos, aplica as regras do sistema e acessa os dados.
- **MongoDB:** guarda os dados de forma permanente.

## Tecnologias

- **Python** (com [FastAPI](https://fastapi.tiangolo.com/), Uvicorn, Pydantic e PyMongo)
- **MongoDB** (rodando localmente, visualizado pelo MongoDB Compass)
- **JavaScript, HTML e CSS** (front end, a fazer)
- **Git e GitHub** para versionamento
- **Postman** e a página `/docs` do FastAPI para testar a API

## Estrutura do projeto

```
livrariaAPIMongoDB-projetopessoal/
├── backend/
│   ├── main.py             # cria a API e liga os grupos de rotas
│   ├── database.py         # conexão com o MongoDB e as coleções
│   ├── schemas.py          # modelos que validam os dados recebidos
│   ├── utils.py            # funções de apoio (ex.: conversão de ids)
│   ├── routers/
│   │   ├── livros.py       # rotas dos livros
│   │   ├── usuarios.py     # rotas dos usuários
│   │   └── emprestimos.py  # rotas dos empréstimos e devoluções
│   ├── requirements.txt    # bibliotecas necessárias
│   ├── teste_conexao.py    # script de estudo: testa a conexão com o MongoDB
│   └── primeiro_livro.py   # script de estudo: guarda um livro no banco
├── frontend/               # interface web (a fazer)
├── docs/                   # documentação do projeto (a fazer)
├── .gitignore
└── README.md
```

## Modelo de dados

O banco se chama `biblioteca` e tem três coleções:

| Coleção       | Campos principais                                                                                         |
|---------------|-----------------------------------------------------------------------------------------------------------|
| `livros`      | `titulo`, `autor`, `ano`, `exemplares`, `disponivel`                                                       |
| `usuarios`    | `nome`, `email`, `data_cadastro`                                                                           |
| `emprestimos` | `livro_id`, `usuario_id`, `data_emprestimo`, `data_prevista_devolucao`, `data_devolucao` (vazia até devolver) |

Cada documento recebe um `_id` gerado pelo MongoDB. O empréstimo não copia os dados do livro e do usuário: guarda apenas os dois ids, que apontam para os documentos das outras coleções.

## Rotas da API

| Método | Rota                            | O que faz                                  |
|--------|---------------------------------|--------------------------------------------|
| GET    | `/`                             | Confirma que a API está no ar              |
| GET    | `/livros`                       | Lista os livros                            |
| POST   | `/livros`                       | Cadastra um livro                          |
| GET    | `/livros/{id}`                  | Busca um livro pelo id                     |
| PATCH  | `/livros/{id}`                  | Atualiza campos de um livro                |
| DELETE | `/livros/{id}`                  | Remove um livro                            |
| GET    | `/usuarios`                     | Lista os usuários                          |
| POST   | `/usuarios`                     | Cadastra um usuário                        |
| GET    | `/emprestimos`                  | Lista os empréstimos                       |
| POST   | `/emprestimos`                  | Registra um empréstimo                     |
| PATCH  | `/emprestimos/{id}/devolucao`   | Registra a devolução de um empréstimo      |

Com a API rodando, a documentação interativa (gerada automaticamente pelo FastAPI) fica em `http://127.0.0.1:8000/docs`.

## Regras do sistema

- Título e autor do livro não podem ser vazios; exemplares não podem ser negativos.
- Um livro com 0 exemplares fica indisponível (`disponivel: false`).
- Dois usuários não podem ter o mesmo e-mail (o e-mail é guardado em minúsculas, sem espaços nas pontas).
- Só é possível emprestar um livro que exista, para um usuário que exista, e que tenha exemplar disponível.
- Cada empréstimo tem prazo de 14 dias e diminui 1 exemplar do livro.
- Cada devolução devolve 1 exemplar ao livro, e um empréstimo não pode ser devolvido duas vezes.

## Como rodar o projeto

### Pré-requisitos

- [Python](https://www.python.org/downloads/) 3.10 ou mais novo
- [MongoDB Community Server](https://www.mongodb.com/try/download/community) rodando em `localhost:27017`
- [Git](https://git-scm.com/)

### Passo a passo (Windows / PowerShell)

1. Clonar o repositório:
   ```
   git clone https://github.com/akemiartxDEV/livrariaAPIMongoDB-projetopessoal.git
   cd livrariaAPIMongoDB-projetopessoal/backend
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

4. Ligar a API (dentro da pasta `backend`, com o ambiente virtual ativo):
   ```
   uvicorn main:app --reload
   ```

5. Abrir a documentação interativa no navegador: `http://127.0.0.1:8000/docs`

O banco `biblioteca` e as coleções são criados automaticamente quando o primeiro dado é guardado.

## Progresso

- [x] Ambiente Python configurado (ambiente virtual e dependências)
- [x] Conexão entre Python e MongoDB
- [x] Projeto versionado no GitHub
- [x] API com FastAPI
- [x] CRUD de livros (cadastrar, listar, buscar, atualizar e remover)
- [x] Cadastro e listagem de usuários
- [x] Empréstimos e devoluções, com controle de estoque
- [x] Código organizado em arquivos (database, schemas, utils e routers)
- [ ] Interface web (front end)
- [ ] Login e proteção das rotas
- [ ] Documentação mais detalhada na pasta `docs/`

## Segurança

Este repositório é público. Hoje o projeto usa um MongoDB local, sem senha, então não há dados sensíveis no código. Se o banco for movido para a nuvem (por exemplo, MongoDB Atlas), o endereço de conexão passa a conter senha e **não** deve ser escrito no código: ele ficará em um arquivo `.env`, que já está listado no `.gitignore`.

## Autoria

Projeto pessoal de estudo, desenvolvido passo a passo com o objetivo de aprender e documentar cada etapa.
Estou fazendo uso do Claude para prosseguir com a programação da API.