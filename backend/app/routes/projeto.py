from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.projeto import Projeto
from app.schemas.projeto import ProjetoResposta, ProjetoCreate, ProjetoUpdate
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteResposta
from app.utils.security import obter_usuario_atual
from app.models.usuario import Usuario

router = APIRouter()


@router.post("/projetos", response_model=ProjetoResposta)
def criar_projeto(projeto: ProjetoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    # antes de criar o projeto, preciso verificar se o cliente_id que veio na requisição existe no banco de dados, para garantir que o projeto seja associado a um cliente válido. Se não existir, retorno um erro 404 dizendo que o cliente associado não foi encontrado.
    cliente_existe= db.query(Cliente).filter(Cliente.id == projeto.cliente_id).first()
    if cliente_existe is None:
        raise HTTPException(status_code=404, detail="Cliente associado não encontrado")
    # o projeto precisa saber qual usuário criou ele, para garantir que cada usuário só veja os projetos que ele criou. O usuário vem do login (Depends(obter_usuario_atual)), e usuario.id é o id dele. Na hora de criar o projeto, a gente passa esse id para o campo usuario_id do projeto, que é uma chave estrangeira para a tabela de usuários.    
    novo_projeto = Projeto(**projeto.dict(), usuario_id=usuario.id)
    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return novo_projeto

@router.get("/projetos", response_model=list[ProjetoResposta])
def listar_projetos(db: Session = Depends(get_db), skip : int = Query(0, ge=0), limit: int = Query(10, ge=1 , le=100),status: str | None = Query(None), cliente_id: int | None = Query(None), usuario: Usuario = Depends(obter_usuario_atual)):
    query = db.query(Projeto)
    query = query.filter(Projeto.usuario_id == usuario.id) # filtra só os projetos onde o usuario_id é igual ao id de quem está logado O usuario vem do login (Depends(obter_usuario_atual)), e usuario.id é o id dele
    if status: # se o usuário passou um status para filtrar
        query = query.filter(Projeto.status == status)
    if cliente_id:# se o usuário passou um cliente_id para filtrar
        query = query.filter(Projeto.cliente_id == cliente_id)
    return query.offset(skip).limit(limit).all()
 

@router.get("/projetos/{id}", response_model=ProjetoResposta)
def listar_projetoUnico(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.usuario_id == usuario.id).first() # filtra só os projetos onde o id da tabela é igual ao id que veio pela URL e pertence ao usuário autenticado
    if projeto is None: 
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto


@router.delete("/projetos/{id}", response_model= ProjetoResposta)
def deletar_projetoId(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.usuario_id == usuario.id).first() # filtra só os projetos onde o id da tabela é igual ao id que veio pela URL e pertence ao usuário autenticado
    if projeto is None: 
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    db.delete(projeto) 
    db.commit() 
    return projeto


@router.put("/projetos/{id}", response_model=ProjetoResposta)
def atualizar_projeto(id: int, dados: ProjetoUpdate, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    projeto= db.query(Projeto).filter(Projeto.id == id, Projeto.usuario_id == usuario.id).first() # filtra só os projetos onde o id da tabela é igual ao id que veio pela URL e pertence ao usuário autenticado
    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if dados.cliente_id is not None:
        cliente_existe = db.query(Cliente).filter(Cliente.id == dados.cliente_id).first()
        if cliente_existe is None:
            raise HTTPException(status_code=404, detail="Cliente associado não encontrado")
               
    for chave, valor in dados.dict(exclude_unset=True).items():
        setattr(projeto, chave, valor)
    db.commit()
    db.refresh(projeto)
    return projeto



@router.get("/projetos/{id}/clientes", response_model=ClienteResposta)
def listar_cliente_projeto(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    projeto = db.query(Projeto).filter(Projeto.id == id, Projeto.usuario_id == usuario.id).first()
    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    cliente = db.query(Cliente).filter(Cliente.id == projeto.cliente_id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente associado não encontrado")
    return cliente