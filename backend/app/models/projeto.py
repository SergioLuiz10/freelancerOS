from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric  # Se um projeto custar R$ 1.500,50 vai dar erro ou perder os centavos.

class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    valor= Column(Numeric(10, 2), nullable=False)  # Alterado para Numeric para suportar valores com centavos
    status= Column(String, nullable=False, default="em_andamento")  # em_andamento / concluido / cancelado
    data_criacao = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False) # chave estrangeira para a tabela clientes

    cliente = relationship("Cliente", back_populates="projetos") # relacionamento com a tabela clientes, onde cada projeto pertence a um cliente