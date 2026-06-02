from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional


# Schemas para validação dos dados de entrada e saída relacionados aos lançamentos financeiros
class LancamentoCreate(BaseModel):
    descricao: str
    valor: Decimal
    tipo: Literal["receita", "despesa"]#so pode ser receita ou despesa
    data_lancamento: datetime
    projeto_id: int


#schema para atualizar um lançamento, onde todos os campos são opcionais usuário pode mandar só os que quer mudar
class LancamentoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[Decimal] = None
    tipo: Optional[Literal["receita", "despesa"]] = None
    data_lancamento: Optional[datetime] = None
    projeto_id: Optional[int] = None


class LancamentoResposta(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str
    data_lancamento: datetime
    data_criacao: datetime
    projeto_id: int
    usuario_id: int
  
   #  permite o Pydantic ler direto de um objeto SQLAlchemy
  class Config:
        from_attributes = True