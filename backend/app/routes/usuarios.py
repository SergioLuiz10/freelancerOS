from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResposta
from app.utils.security import hash_senha

router = APIRouter()

# Endpoint para criar um novo usuário
@router.post("/usuariosRegister", response_model=UsuarioResposta)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existe = db.query(Usuario).filter(Usuario.email == dados.email).first()# verifica se já existe um usuário com o email fornecido no banco de dados
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Email já registrado")
    senha_hasheada = hash_senha(dados.senha)
    novo_usuario = Usuario(email=dados.email, senha_hash=senha_hasheada)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

    

 