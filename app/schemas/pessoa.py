from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import date

from models.pessoa import Pessoa

#
# schemas 
#

class PessoaAddSchema(BaseModel):
    apelido: constr(max_length=32)
    nome : constr(max_length=100)
    nascimento : date
    stack : Optional[List[constr(max_length=32)]] = None

class PessoaViewSchema(PessoaAddSchema):
    id: constr(max_length=36)
	
PessoaListViewSchema = List[PessoaViewSchema] 

class PessoaSearchSchema(BaseModel):
    search_term: str

#
# helpers
#

def PessoaRepresentation(pessoa: Pessoa):
    return {
    	"id": pessoa.id,
        "apelido": pessoa.apelido,
        "nome": pessoa.nome,
        "nascimento": pessoa.nascimento,
        "stack": list(pessoa.stack.split(" "))
    }

def PessoaListRepresentation(pessoas: List[Pessoa]):
    return [PessoaRepresentation(p) for p in pessoas]

def ErrorRepresentation(status_code, message):
    return {
    	"status": status_code,
        "message": message
    }

