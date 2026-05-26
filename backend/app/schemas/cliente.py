from pydantic import BaseModel #  criar modelos de dado 
from typing import Optional # para campos opcionais
from datetime import datetime # para lidar com datas

#herda de BaseModel. Ela vai conter os campos básicos de um cliente
class ClienteBase(BaseModel): 
    nome: str # nome é obrigatório e deve ser uma string
    email: str # email é obrigatório e deve ser uma string
    telefone: str # telefone é obrigatório e deve ser uma string
 

# Usada quando alguém cria um cliente via POST. Herda tudo da Base, sem adicionar nada novo por enquanto.
class ClienteCreate(ClienteBase):
    pass


# Usada quando alguém atualiza um cliente via PUT. Campos opcionais para atualizar só o que for enviado.
class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None


# quando algm busca um cliente 
class ClienteResposta(ClienteBase):
    id: int #  vai incluir o id do cliente pq quando buscamos um cliente, queremos ver o id dele também e como n tem no ClienteBase, a gente cria essa classe ClienteResposta que herda de ClienteBase e adiciona o campo id.
    data_criacao: datetime    
    class Config:
        from_attributes = True# ler os dados de objetos também, não só de dicionários.
 