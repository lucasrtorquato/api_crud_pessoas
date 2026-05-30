from sqlalchemy import Column, Integer, String, Text

from database import Base


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(100))
    sobrenome = Column(String(100))
    email = Column(String(150))
    whatsapp = Column(String(20))

    cep = Column(String(10))
    rua = Column(String(200))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(2))

    observacoes = Column(Text)