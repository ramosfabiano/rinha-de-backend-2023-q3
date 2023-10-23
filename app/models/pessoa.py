from sqlalchemy import Column, String, Integer, Date, ARRAY
from models.base import Base


class Pessoa(Base):

    __tablename__ = 'pessoas'

    id = Column(String(36), primary_key=True)
    apelido = Column(String(32), unique=True)
    nome = Column(String(100), unique=False)
    nascimento = Column(String(10), unique=False) #AAAA-MM-DD
    stack = Column(ARRAY(String(32)), unique=False)

    @property
    def stack(self) -> str:
        return ' '.join(self.stack) if self.stack else None
                       
    def __init__(self, apelido, nome, nascimento, stack):
        self.apelido = apelido
        self.nome = nome
        self.nascimento = nascimento
        self.stack = stack
