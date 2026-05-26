from fastapi import FastAPI
from app.database import engine 
from sqlalchemy import text # permite escrever SQL puro dentro do Python
from app.database import Base # importa a classe Base do arquivo database.py para criar as tabelas no banco de dados
from app.routes.clientes import router as clientes_router # importa o router de clientes para incluir no aplicativo FastAPI
from app.routes.projeto import router as projetos_router # importa o router de projetos para incluir no aplicativo FastAPI
from app.routes.auth import router as auth_router
from app.routes.usuarios import router as usuarios_router
app = FastAPI()
app.include_router(clientes_router) # inclui as rotas de clientes no aplicativo FastAPI
app.include_router(projetos_router) # inclui as rotas de projetos no aplicativo FastAPI
app.include_router(auth_router, tags=["Autenticação"]) # inclui as rotas de autenticação no aplicativo FastAPI e adiciona uma tag "Autenticação" para organizar as rotas relacionadas à autenticação na documentação automática do FastAPI
app.include_router(usuarios_router) # inclui as rotas de usuários no aplicativo FastAPI  
@app.get("/")
def root():
    return {"mensagem": "FreelancerOS rodando!"}

@app.get("/test-db")
def test_db():
    with engine.connect() as conn: # conecta com o banco de dados usando o engine (with garante que a conexão seja fechada depois de usar)
        result = conn.execute(text("SELECT 1")) # executa uma consulta SQL simples para testar a conexão
        return {"result": str(result.fetchone())} # retorna o resultado da consulta, que deve ser  
 

Base.metadata.create_all(bind=engine) # ela olha todos os Models que herdam do Base (como o Cliente) usar o engine pra conectar  