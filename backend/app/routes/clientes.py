from fastapi import APIRouter , Depends, HTTPException, Query # o Depends é permite injetar dependências nas rotas(como a sessão do banco de dados)
from sqlalchemy.orm import Session#toda vez que a API precisar ler ou salvar algo no banco abre uma Session, faz o que precisa, e fecha. 
from app.database import get_db # importa a função que abre e fecha a sessão com o banco
from app.models.cliente import Cliente # importa a classe Cliente do arquivo cliente.py para usar na criação e consulta de clientes
from app.schemas.cliente import ClienteResposta , ClienteCreate, ClienteUpdate # importa o esquema de resposta do cliente para usar nas rotas de clientes
from app.models.projeto import Projeto # importa a classe Projeto do arquivo projeto.py para usar no relacionamento entre clientes e projetos
from app.schemas.projeto import ProjetoResposta # importa o esquema de resposta do projeto para usar nas rotas de projetos, principalmente para mostrar os projetos associados a um cliente
from app.utils.security import obter_usuario_atual
from app.models.usuario import Usuario


#na hora de jogar no main usar o app.include_router para incluir as rotas de clientes no aplicativo FastAPI principal.
router = APIRouter()

@router.post("/clientes", response_model=ClienteResposta)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    novo_cliente = Cliente(**cliente.dict()) # cria um novo cliente usando os dados recebidos na requisição. O **cliente.dict() pega os dados do cliente e transforma em argumentos para criar o objeto Cliente.
    db.add(novo_cliente) # adiciona o novo cliente à sessão do banco de dados
    db.commit() # salva as mudanças no banco de dados
    db.refresh(novo_cliente) # após salvar, o banco gera alguns dados automaticamente, como o id do cliente
    return novo_cliente # retorna o cliente criado, incluindo o id gerado pelo banco de dados


@router.get("/clientes", response_model=list[ClienteResposta])
def listar_clientes(db: Session = Depends(get_db), skip : int = Query(0, ge=0), limit: int = Query(10, ge=1 , le=100),nome: str | None = Query(None), usuario: Usuario = Depends(obter_usuario_atual)):#(vem na URL depois do ?)se usuário não passar, começa 0) e um limite de quantos clientes retornar (padrão 10, mínimo 1, máximo 100) e um filtro opcional para o nome do cliente (se passar, filtra os clientes pelo nome, se não passar, retorna todos os clientes)
    query = db.query(Cliente) # inicia a consulta para buscar os clientes no banco de dados
    if nome: # se o usuário passou um nome para filtrar
        query = query.filter(Cliente.nome.ilike(f"%{nome}%")) # filtra os clientes onde o nome contém a string passada (case-insensitive)
    return query.offset(skip).limit(limit).all() # aplica o skip e limit para paginar os resultados e retorna a lista de clientes encontrados

@router.get("/clientes/{id}", response_model=ClienteResposta)   
def listar_clienteUnico(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first() #filtra só os clientes onde o id da tabela é igual ao id que veio pela URL
    if cliente is None: # se não encontrar nenhum cliente com aquele id, retorna um erro 404
         raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente # se encontrar, retorna o cliente encontrado


@router.put("/clientes/{id}", response_model=ClienteResposta)
def atualizar_cliente(id: int, dados: ClienteUpdate, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for campo, valor in dados.dict(exclude_unset=True).items(): # percorre só os campos que foram enviados na requisição
        setattr(cliente, campo, valor) # atualiza cada campo do cliente com o novo valor
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/clientes/{id}", response_model= ClienteResposta) # precisa do cleinte resposta para retornar o cliente deletado
def deletar_clienteId(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first() # filtra só os clientes onde o id da tabela é igual ao id que veio pela URL
    if cliente is None: # se não encontrar nenhum cliente com aquele id, retorna um erro 404
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente) # deleta o cliente encontrado
    db.commit() # salva as mudanças no banco de dados
    return cliente # retorna o cliente deletado


# rota para listar os projetos associados a um cliente específico, usando o relacionamento definido entre as tabelas Cliente e Projeto. O id do cliente é passado pela URL, e a resposta é uma lista de projetos associados a esse cliente.
@router.get("/clientes/{id}/projetos", response_model=list[ProjetoResposta])  
def listar_projetos_cliente(id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obter_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first() # filtra só os clientes onde o id da tabela é igual ao id que veio pela URL
    if cliente is None: # se não encontrar nenhum cliente com aquele id, retorna um erro 404
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db.query(Projeto).filter(Projeto.cliente_id == id).all() # consulta todos os projetos onde o cliente_id é igual ao id do cliente passado pela URL e retorna como uma lista