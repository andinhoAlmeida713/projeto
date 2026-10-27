from fastapi import FastAPI
from contextlib import asynccontextmanager
from entidades.aluno import aluno_router
from dependencies.dependencies import database

# ----------------------------------------------------------------------------
# GERENCIAMENTO DE CICLO DE VIDA (Lifespan)
# Abre o túnel SSH ao iniciar a API e fecha ao desligar o servidor.
# ----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado ao Iniciar o FastAPI
    print("Iniciando a aplicação e conectando ao túnel SSH...")
    # Se você quiser que o SQLModel crie as tabelas automaticamente no MySQL remoto:
    # database.criar_tabelas() 
    yield
    # Código executado ao Desligar o FastAPI
    print("Desligando a aplicação e encerrando o túnel SSH...")
    database.stop_tunnel()


# Inicialização do FastAPI com o Lifespan configurado
app = FastAPI(
    title="API de Gerenciamento de Alunos",
    version="1.0.0",
    lifespan=lifespan
)

# ----------------------------------------------------------------------------
# REGISTRO DE ROTAS
# ----------------------------------------------------------------------------
# Adiciona as rotas de Aluno à aplicação principal com um prefixo opcional
app.include_router(aluno_router, prefix="/api/v1", tags=["Alunos"])


# Endpoint raiz apenas para verificar se a API está online
@app.get("/", tags=["Status"])
def root():
    return {"status": "API Online", "mensagem": "Sistema adaptado para Alunos com sucesso!"}
