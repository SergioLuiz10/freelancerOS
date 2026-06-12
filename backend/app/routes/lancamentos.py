from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.lancamento import Lancamento  # pra inserir e consultar lançamentos.
from app.models.projeto import (
    Projeto,
)  # usar lá no POST pra checar se o projeto_id existe e é seu
from app.models.usuario import (
    Usuario,
)  # usar lá no POST pra pegar o id do usuário logado e colocar no lançamento
from app.schemas.lancamento import (
    LancamentoCreate,
    LancamentoResposta,
    LancamentoUpdate,
)  # pra validar os dados de entrada e saída dos lançamentos
from app.database import get_db  # pra pegar a sessão do banco de dados
from app.auth import obter_usuario_atual_endpoint

#  todas as rotas desse arquivo já começam com /lancamentos
router = APIRouter(prefix="/lancamentos", tags=["lancamentos"])


@router.post(
    "/", response_model=LancamentoResposta, status_code=status.HTTP_201_CREATED
)
def criar_lancamento(
    dados: LancamentoCreate,  # json que vem na requisição para criar um lançamento, validado pelo esquema LancamentoCreate
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(
        obter_usuario_atual_endpoint
    ),  # quem tá logado, via token
):
    # pegar o mesmo projeto vindo do endpoint
    projeto_consulta = (
        db.query(Projeto)
        .filter(
            Projeto.id
            == dados.projeto_id,  # quero o projeto cujo id seja igual ao que o usuário mandou
            Projeto.usuario_id
            == usuario_atual.id,  # o projeto tem que pertencer ao usuário logado, pra garantir que cada usuário só veja os projetos que ele criou
        )
        .first()
    )
    if (
        projeto_consulta is None
    ):  # se n tiver projeto no id q o usuario mandou , vem erro
        raise HTTPException(status_code=404, detail="Projeto associado não encontrado")
    # se tiver projeto, cria o lançamento normalmente, associando ele ao projeto encontrado e ao usuário logado
    novo_lancamento = Lancamento(
        descricao=dados.descricao,
        valor=dados.valor,
        tipo=dados.tipo,
        data_lancamento=dados.data_lancamento,
        projeto_id=dados.projeto_id,
        usuario_id=usuario_atual.id,  # o lançamento também tem que pertencer ao usuário logado, pra garantir que cada usuário só veja os lançamentos que ele criou
    )
    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)
    return novo_lancamento

@router.get("/{lancamento_id}", response_model=LancamentoResposta)
def obter_lancamento(lancamento_id: int, db: Session = Depends(get_db), usuario_atual: Usuario = Depends(obter_usuario_atual_endpoint)):
    lancamento=db.query(Lancamento).filter(Lancamento.id == lancamento_id, Lancamento.usuario_id == usuario_atual.id).first() # filtra só os lançamentos onde o id da tabela é igual ao id que veio pela URL e pertence ao usuário autenticado
    if lancamento is None: #se n encontrar nenhum lancamento com o id vindo do lancamento_id lanca erro 
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    return lancamento

#
@router.get("/", response_model=list[LancamentoResposta])
def listar_lancamentos(db: Session = Depends(get_db), usuario_atual:Usuario = Depends(obter_usuario_atual_endpoint)):
    lancamento = db.query(Lancamento).filter(Lancamento.usuario_id==usuario_atual.id).all()
   
    return lancamento


@router.delete("/{lancamento_id}", response_model=LancamentoResposta)
def deletar_lancamento(lancamento_id: int, db: Session = Depends(get_db), usuario_atual: Usuario = Depends(obter_usuario_atual_endpoint)):
    lancamento = db.query(Lancamento).filter(Lancamento.id == lancamento_id, Lancamento.usuario_id == usuario_atual.id).first() # filtra só os lançamentos onde o id da tabela é igual ao id que veio pela URL e pertence ao usuário autenticado
    if lancamento is None: #se n encontrar nenhum lancamento com o id vindo do lancamento_id lanca erro
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    db.delete(lancamento) #deleta o lançamento encontrado
    db.commit() #confirma a deleção no banco de dados
    return lancamento #retorna o lançamento deletado
