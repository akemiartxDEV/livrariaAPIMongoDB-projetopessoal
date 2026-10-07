from fastapi import FastAPI

from routers.livros import router as livros_router
from routers.usuarios import router as usuarios_router
from routers.emprestimos import router as emprestimos_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Biblioteca",
    description="API de estudo para registrar livros, usuários e empréstimos de uma biblioteca.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(livros_router)
app.include_router(usuarios_router)
app.include_router(emprestimos_router)

@app.get("/")
def raiz():
    return {"mensagem": "API da biblioteca funcionando"}