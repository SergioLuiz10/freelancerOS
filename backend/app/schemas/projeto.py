from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProjetoBase(BaseModel):
    nome: str
    descricao: str
    valor: Decimal
    status: Optional[str] = "em_andamento"  # Valor padrão para status
    cliente_id: int  # ID do cliente associado ao projeto

# Usada para criar um projeto via POST. Herda tudo da Base, sem adicionar nada novo por enquanto.
class ProjetoCreate(ProjetoBase):
    pass


class ProjetoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    status: Optional[str] = None
    cliente_id: Optional[int] = None

class ProjetoResposta(ProjetoBase):
    data_criacao: datetime

    class Config:
        from_attributes = True 

