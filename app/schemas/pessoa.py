from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import date

from models.pessoa import Pessoa

#
# schemas 
#

# os campos apelido, nome, nascimento estão como opcionais aqui no esquema da requisição
# mas são obrigatórios no modelo. Isso é necessário para que o erro seja 422 , e não 400,
# quando os mesmos forem enviados como nulos na requisição (conforme especificação do desafio...)
class PessoaAddSchema(BaseModel):
    apelido: Optional[constr(max_length=32)]
    nome : Optional[constr(max_length=100)]
    nascimento : Optional[date]
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
        "stack": list(pessoa.stack.split(" ")) if pessoa.stack else None
    }

def PessoaRepresentationEx(id: str, apelido: str, nome: str, nascimento: date, stack: List[str]):
    return {
    	"id": id,
        "apelido": apelido,
        "nome": nome,
        "nascimento": nascimento.strftime('%Y-%m-%d'),
        "stack": None if (stack is None or len(stack) == 0) else [s for s in stack if s]
    }

def PessoaListRepresentation(pessoas: List[Pessoa]):
    return [PessoaRepresentation(p) for p in pessoas]

def ErrorRepresentation(status_code, message):
    return {
    	"status": status_code,
        "message": message
    }

