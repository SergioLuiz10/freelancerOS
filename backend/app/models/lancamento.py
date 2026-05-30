from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func # a usar a função de data e hora atual do banco de dados
from app.database import Base # importa a classe Base do arquivo database.py para criar as tabelas


# o lançamento tem que saber a qual projeto ele pertence, então tem que ter uma chave estrangeira para a tabela de projetos. O projeto_id é um inteiro que referencia o id da tabela de projetos. O relacionamento entre as tabelas é feito através do ForeignKey, onde o projeto_id é uma chave estrangeira que referencia o id da tabela de projetos.
class Lancamento(Base):

    __tablename__ = "lancamentos"

    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao= Column(String, nullable=False)
    valor= Column(Numeric(10, 2), nullable=False) # Alterado para Numeric para suportar valores com centavos
    tipo= Column(String, nullable=False) # receita ou despesa
    data_criacao = Column(DateTime(timezone=True), server_default=func.now()) 

    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False) # chave estrangeira para a tabela de projetos, indicando a qual projeto o lançamento pertence
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False) # chave estrangeira para a tabela de usuários, indicando qual usuário criou o lançamento