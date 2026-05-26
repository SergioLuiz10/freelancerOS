from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

 


class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResposta(BaseModel):
    id: int
    email: EmailStr
    criado_em: datetime

    class Config:
        from_attributes = True        