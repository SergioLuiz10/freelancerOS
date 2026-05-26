from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm# Importa o formulário de autenticação do OAuth2
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.utils.security import verificar_senha, criar_token_acesso, decodificar_token_acesso, obter_usuario_atual


router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first() #  busca o usuário no banco de dados usando o email fornecido no formulário de autenticação
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash): #  verifica se o usuário existe e se a senha fornecida corresponde ao hash armazenado
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos") #  se o usuário não for encontrado, retorna um erro de autenticação
    token_acesso = criar_token_acesso({"sub": usuario.email}) #  se a autenticação for bem-sucedida, cria um token de acesso JWT com o email do usuário como assunto (sub)
    return {"access_token": token_acesso, "token_type": "bearer"} #  retorna o token de acesso gerado e o tipo de token (bearer)

# Endpoint para obter informações do usuário autenticado
@router.get("/me") 
def obter_usuario_atual_endpoint(usuario: Usuario = Depends(obter_usuario_atual)):
    return {"email": usuario.email, "id": usuario.id} #  retorna as informações do usuário autenticado, incluindo email , id e data de criação