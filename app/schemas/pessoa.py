from pydantic import BaseModel, constr
from datetime import date
from typing import List, Optional

from models.pessoa import Pessoa

#
# schemas 
#

class PessoaAddSchema(BaseModel):
    apelido: str
    nome : str
    nascimento : str
    stack : Optional[List[constr(max_length=32)]] = None

class PessoaViewSchema(PessoaAddSchema):
    id: str
	
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
        "stack": pessoa.stack
    }

def PessoaListRepresentation(pessoas: List[Pessoa]):
    return [PessoaRepresentation(p) for p in pessoas]
    

