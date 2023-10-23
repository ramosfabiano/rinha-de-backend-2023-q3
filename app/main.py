from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from typing import List
import json

from models import *
from schemas import *

# see 
#	https://fastapi.tiangolo.com/
#   https://fastapi.tiangolo.com/tutorial/handling-errors/
#   https://fastapi.tiangolo.com/tutorial/response-model/

app = FastAPI()

@app.get("/")
async def hello():
    return {"healthy": "yes"};
    
#
# teste somente, remover
# 
@app.get("/pessoas", response_model=PessoaListViewSchema, status_code=200)
async def lista_pessoas():
    try:
        p1 = Pessoa('id1','x','x','2023-10-01', ['C++', 'Java']);
        p2 = Pessoa('id2','y','y','2023-10-02', ['JS', 'Python']); 
        pessoas = [p1, p2]
        return PessoaListRepresentation(pessoas)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal server error')

                      
'''
@app.get("/pessoas/{id}")               #200, 404
async def retorna_pessoa(id: int):
    # TODO: implementar

@app.post("/pessoas")
async def cria_pessoa(pessoa: Pessoa):  #201, 400, 422
    # TODO: implementar

@app.get("/pessoas")
async def busca_pessoas(termo: str):     #200, 400
    # TODO: implementar

@app.get("/contagem-pessoas")
async def conta_pessoas():               #200
    """
    Retorna a contagem de pessoas cadastradas.
    """
    # Implementação não fornecida
'''


