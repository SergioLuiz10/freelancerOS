from sqlalchemy import create_engine # é a função que vai criar a conexão com o banco
from sqlalchemy.orm import sessionmaker , declarative_base #  cria tableas no banco e fecha conversa com banco 
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_Banco = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_Banco) 
SessionLocal = sessionmaker(bind= engine) #     criar a sessão de conexão com o banco e bind é   ligar a sessão com o engine
Base = declarative_base() # é a função que vai criar as tabelas no banco

#abre e fecha a sessão
def get_db():
    db = SessionLocal() # cria uma nova sessão de conexão com o banco
    try:
        yield db # yield é usado para criar um gerador, que permite usar a função get_db como uma dependência nas rotas do FastAPI. Ele fornece a sessão do banco de dados para as rotas e garante que a sessão seja fechada corretamente após o uso.
    finally:
        db.close() # fecha a sessão de conexão com o banco, garantindo que os recursos sejam liberados mesmo se ocorrer um erro durante o uso da sessão.