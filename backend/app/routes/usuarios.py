from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResposta
from app.utils.security import hash_senha, obter_usuario_atual

router = APIRouter()

# Endpoint para criar um novo usuário
@router.post("/usuariosRegister", response_model=UsuarioResposta)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existe = db.query(Usuario).filter(Usuario.email == dados.email).first() # verifica se já existe um usuário com o email fornecido no banco de dados
    if usuario_existe:
        raise HTTPException(status_code=400, detail="Email já registrado")
    senha_hasheada = hash_senha(dados.senha)
    novo_usuario = Usuario(email=dados.email, senha_hash=senha_hasheada)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


# Endpoint para listar todos os usuários
@router.get("/usuarios", response_model=list[UsuarioResposta])
def listar_usuarios(db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    return db.query(Usuario).all() # retorna todos os usuários cadastrados no banco de dados


# Endpoint para buscar um usuário pelo id
@router.get("/usuarios/{id}", response_model=UsuarioResposta)
def buscar_usuario(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    usuario_encontrado = db.query(Usuario).filter(Usuario.id == id).first() # busca o usuário pelo id no banco de dados
    if usuario_encontrado is None: # se não encontrar, retorna erro 404
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_encontrado


# Endpoint para atualizar os dados de um usuário pelo id
@router.put("/usuarios/{id}", response_model=UsuarioResposta)
def atualizar_usuario(id: int, dados: UsuarioCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    usuario_encontrado = db.query(Usuario).filter(Usuario.id == id).first() # busca o usuário pelo id no banco de dados
    if usuario_encontrado is None: # se não encontrar, retorna erro 404
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario_encontrado.email = dados.email # atualiza o email do usuário
    usuario_encontrado.senha_hash = hash_senha(dados.senha) # atualiza a senha já hasheada do usuário
    db.commit()
    db.refresh(usuario_encontrado)
    return usuario_encontrado


# Endpoint para deletar um usuário pelo id
@router.delete("/usuarios/{id}", response_model=UsuarioResposta)
def deletar_usuario(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    usuario_encontrado = db.query(Usuario).filter(Usuario.id == id).first() # busca o usuário pelo id no banco de dados
    if usuario_encontrado is None: # se não encontrar, retorna erro 404
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(usuario_encontrado) # deleta o usuário encontrado
    db.commit() # salva as mudanças no banco de dados
    return usuario_encontrado # retorna o usuário deletado
