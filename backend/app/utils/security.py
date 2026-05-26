import os
from dotenv import load_dotenv # biblioteca para carregar variáveis de ambiente a partir de um arquivo .env
from passlib.context import CryptContext #  biblioteca passlib para lidar com a criptografia de senhas
from datetime import datetime, timedelta , timezone # biblioteca para lidar com datas e horários, usada para definir a expiração dos tokens de acesso 
from jose import JWTError, jwt # biblioteca para lidar com JSON Web Tokens (JWT), usada para criar e verificar tokens de acesso
from fastapi import Depends, HTTPException, status #  biblioteca FastAPI para lidar com dependências, exceções HTTP e status de resposta
from fastapi.security import OAuth2PasswordBearer#  utenticação usando o esquema OAuth2 com senhas 
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario

load_dotenv() # carrega as variáveis de ambiente do arquivo .env
#   deprecated="auto" indica que o passlib deve marcar automaticamente os hashes antigos como obsoletos se eles não usarem o esquema atual.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  


SECRET_KEY = os.getenv("SECRET_KEY") # obtém a chave secreta do arquivo .env para criptografia e segurança
ALGORITHM = os.getenv("ALGORITHM") # obtém o algoritmo de criptografia do arquivo .env para gerar tokens de acesso
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # obtém o tempo de expiração dos tokens de acesso do arquivo .env, com um valor padrão de 30 minutos se a variável não estiver definida
auth_scheme = OAuth2PasswordBearer(tokenUrl="login") #o endpoint de login para obter tokens de acesso

# Função para gerar o hash da senha usando bcrypt
def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha) #  gera um hash da senha usando o esquema bcrypt

# Função para verificar se a senha fornecida corresponde ao hash armazenado
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash) #  verifica se a senha fornecida corresponde ao hash armazenado

# Função para criar um token de acesso JWT com os dados fornecidos
def criar_token_acesso(data: dict) -> str:
    to_encode = data.copy() #  cria uma cópia dos dados fornecidos para codificar no token
    expireEM= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #  define a data de expiração do token com base no tempo atual e no tempo de expiração configurado
    dados_pra_codificar = {"exp": expireEM, "sub": to_encode.get("sub")} #  cria um dicionário com os dados a serem codificados no token, incluindo a data de expiração e o assunto (sub)
    token = jwt.encode(dados_pra_codificar, SECRET_KEY, algorithm=ALGORITHM) #  codifica os dados usando a chave secreta e o algoritmo de criptografia configurados
    return token #  retorna o token de acesso gerado

# Função para decodificar um token de acesso JWT e retornar os dados contidos pra api o token
def decodificar_token_acesso(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #  decodifica o token usando a chave secreta e o algoritmo de criptografia configurados
        return payload #  retorna os dados decodificados do token
    except JWTError:
        return None #  se ocorrer um erro durante a decodificação do token, retorna None


# Função para obter o usuário atual com base no token de acesso fornecido
def obter_usuario_atual(token:str = Depends(auth_scheme), db: Session = Depends(get_db))-> Usuario: 
    payload = decodificar_token_acesso(token) #  decodifica o token de acesso para obter os dados contidos nele
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de acesso inválido") #  se o token for inválido, retorna um erro de autenticação
    email = payload.get("sub") #  obtém o email do usuário a partir dos dados decodificados do token
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de acesso inválido") #  se o email não estiver presente nos dados do token, retorna um erro de autenticação
    usuario = db.query(Usuario).filter(Usuario.email == email).first() #  consulta o banco de dados para obter o usuário com base no email
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado") #  se o usuário não for encontrado no banco de dados, retorna um erro de autenticação
    return usuario #  retorna o usuário encontrado no banco de dados    