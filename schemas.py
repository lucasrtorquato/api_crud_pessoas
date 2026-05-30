from pydantic import BaseModel, EmailStr
from typing import Optional


class PessoaBase(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr
    whatsapp: str

    cep: str
    rua: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str

    observacoes: Optional[str] = None


class PessoaCreate(PessoaBase):
    pass


class PessoaUpdate(PessoaBase):
    pass


class PessoaResponse(PessoaBase):
    id: int

    class Config:
        from_attributes = True