from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func# a usar a função de data e hora atual do banco de dados  
from app.database import Base# importa a classe Base do arquivo database.py para criar as tabelas no banco de dados

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now()) 


      