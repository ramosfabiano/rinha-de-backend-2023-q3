from sqlalchemy import Column, String, Integer, Date, ARRAY, text
from models.base import Base
from datetime import date
import uuid

class Pessoa(Base):

    __tablename__ = 'pessoas'

    # pré-criada em table.sql
    # o campo "termo" é auto-gerado para agilizar a busca por termo
    id = Column(String(36), primary_key=True)
    apelido = Column(String(32), unique=True, nullable=False)
    nome = Column(String(100), unique=False, nullable=False)
    nascimento = Column(String(10), unique=False, nullable=False)
    stack = Column(String(2048), unique=False, nullable=True)
    termo = Column(String(), server_default=text("LOWER(CONCAT(apelido, ' ', nome, COALESCE(CONCAT(' (', stack, ')'), '')))"))

    def __init__(self, apelido, nome, nascimento, stack):
        self.id = str(uuid.uuid4())
        self.apelido = apelido
        self.nome = nome
        self.nascimento = nascimento
        self.stack = ' '.join(filter(None,stack)) if stack else None 
