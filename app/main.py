from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from typing import List
import json
from datetime import date
import redis
from cachetools import cached, TTLCache 

from models import *
from schemas import *

# main app
app = FastAPI()

# Redis cache
redis_client = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], password=os.environ['REDIS_PASSWORD'], db=0)

# exception handler global para os casos de falha de validação do schema do request
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exception):
    return JSONResponse(status_code=400, content=ErrorRepresentation(400, 'Bad request'))

# docs
@app.get("/")
async def hello():
    return RedirectResponse(url='/docs')
 
'''
curl -v -X 'POST'   'http://localhost:8081/pessoas'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "apelido": "snowj",
  "nome": "John Snow",
  "nascimento": "1986-12-26",
  "stack": ["C++", "Python"]
}' | jq
'''
@app.post("/pessoas", response_model=PessoaViewSchema, status_code=201)
async def cria_pessoa(pessoa: PessoaAddSchema):
    try:
        session = Session()
        p = Pessoa(pessoa.apelido, pessoa.nome, pessoa.nascimento, pessoa.stack)
        session.add(p)
        session.commit()
        session.refresh(p)
        session.close()
        response = PessoaRepresentation(p)
        redis_client.set(f'id:{p.id}', json.dumps(response)) 
        return JSONResponse(status_code=201, content=response, headers={'Location': f'/pessoas/{p.id}'})
    except IntegrityError:
        return JSONResponse(status_code=422, content=ErrorRepresentation(422, 'Unprocessable entity/content'))
    except Exception as e:
        return JSONResponse(status_code=500, content=ErrorRepresentation(500, 'Internal server error'))

'''
curl -v -X 'GET' 'http://localhost:8081/pessoas/c25efe45-36f4-45a0-adbb-4093642c4968' -H 'accept: application/json' | jq
'''  
@app.get("/pessoas/{id}", response_model=PessoaViewSchema, status_code=200)
async def retorna_pessoa(id: str):
    try:
        cached_pessoa = redis_client.get(f'id:{id}')
        if cached_pessoa is None: 
            session = Session()
            p = session.query(Pessoa).filter(Pessoa.id == id).first()
            session.close()
            if p is None:
                return JSONResponse(status_code=404, content=ErrorRepresentation(404, 'Not found')) 
            response = PessoaRepresentation(p)
            redis_client.set(f'id:{id}', json.dumps(response)) 
        else:
            response = json.loads(cached_pessoa)
        return JSONResponse(response)   
    except Exception as e:
        return JSONResponse(status_code=500, content=ErrorRepresentation(500, 'Internal server error'))

'''
curl -v -X 'GET' 'http://localhost:8081/pessoas?t=python' -H 'accept: application/json' | jq
'''
@app.get("/pessoas", response_model=PessoaListViewSchema, status_code=200)
async def busca_pessoas(t: str):
    try:
        session = Session()
        # spec: A busca não precisa ser paginada e poderá retornar apenas os 50 primeiros registros 
        p = session.query(Pessoa).filter(or_(Pessoa.apelido.ilike(f'%{t}%'),Pessoa.nome.ilike(f'%{t}%'),Pessoa.stack.ilike(f'%{t}%'))).limit(50).all()
        session.close()
        # spec: O status code deverá ser sempre 200 - Ok, mesmo para o caso da busca não retornar resultados (vazio).
        if p is None:
            p = []
        return JSONResponse(PessoaListRepresentation(p))
    except Exception as e:
        return JSONResponse(status_code=500, content=ErrorRepresentation(500, 'Internal server error'))


'''
curl -v -X 'GET' 'http://localhost:8081/contagem-pessoas' 
'''
@app.get("/contagem-pessoas", response_model=str, status_code=200)
async def conta_pessoas(): 
    try:
        session = Session()
        p = session.query(Pessoa).count()
        session.close()
        return PlainTextResponse(str(p))
    except Exception as e:
        return JSONResponse(status_code=500, content=ErrorRepresentation(500, 'Internal server error'))
