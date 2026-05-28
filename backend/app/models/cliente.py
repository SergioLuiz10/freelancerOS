from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime # para pegar a data atual
from app.database import Base # importa a classe Base do arquivo database.py
from sqlalchemy.orm import relationship          # <-- adicionar isso

class Cliente(Base):
    __tablename__ = "clientes" # nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True, autoincrement=True ) # id é a chave primária e é um inteiro
    nome = Column(String, nullable=False) # nome é uma string e não pode ser nulo
    email = Column(String, unique=True, index=True, nullable=False) # email é uma string, deve ser único, indexado e não pode ser nulo
    telefone = Column(String, nullable=False) # telefone é uma string e não pode ser nulo
    data_criacao = Column(DateTime, default=datetime.utcnow) # data_criacao é um DateTime e tem como valor padrão a data atual
   
        #o valor aqui dentro tem que ser um id que existe na tabela usuarios
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False) # chave estrangeira para a tabela de usuários, indicando qual usuário criou o cliente
    projetos = relationship("Projeto", back_populates="cliente") # relacionamento com a tabela projetos, onde cada cliente pode ter vários projetos
