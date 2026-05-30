from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import SessionLocal
from database import engine
from database import Base

from models import Pessoa

from schemas import (
    PessoaCreate,
    PessoaUpdate,
    PessoaResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Cadastro de Pessoas",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "mensagem": "API de Cadastro de Pessoas"
    }


@app.post(
    "/pessoas",
    response_model=PessoaResponse
)
def criar_pessoa(
    pessoa: PessoaCreate,
    db: Session = Depends(get_db)
):

    nova_pessoa = Pessoa(**pessoa.model_dump())

    db.add(nova_pessoa)
    db.commit()
    db.refresh(nova_pessoa)

    return nova_pessoa


@app.get(
    "/pessoas",
    response_model=list[PessoaResponse]
)
def listar_pessoas(
    db: Session = Depends(get_db)
):

    return db.query(Pessoa).all()


@app.get(
    "/pessoas/{id}",
    response_model=PessoaResponse
)
def buscar_pessoa(
    id: int,
    db: Session = Depends(get_db)
):

    pessoa = db.query(Pessoa).filter(
        Pessoa.id == id
    ).first()

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    return pessoa


@app.put(
    "/pessoas/{id}",
    response_model=PessoaResponse
)
def atualizar_pessoa(
    id: int,
    dados: PessoaUpdate,
    db: Session = Depends(get_db)
):

    pessoa = db.query(Pessoa).filter(
        Pessoa.id == id
    ).first()

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    for campo, valor in dados.model_dump().items():
        setattr(pessoa, campo, valor)

    db.commit()
    db.refresh(pessoa)

    return pessoa


@app.delete("/pessoas/{id}")
def excluir_pessoa(
    id: int,
    db: Session = Depends(get_db)
):

    pessoa = db.query(Pessoa).filter(
        Pessoa.id == id
    ).first()

    if not pessoa:
        raise HTTPException(
            status_code=404,
            detail="Pessoa não encontrada"
        )

    db.delete(pessoa)
    db.commit()

    return {
        "mensagem": "Pessoa removida com sucesso"
    }