from fastapi import FastAPI
import json

from models import *
from schemas import *

# see 
#	https://fastapi.tiangolo.com/
#   https://fastapi.tiangolo.com/tutorial/handling-errors/
#
app = FastAPI()

@app.get("/")
async def hello():
    return {"healthy": "yes"};
    
'''    
@app.post("/pessoas")
async def cria_pessoa(pessoa: Pessoa):  #201, 400, 422
    """
    Cria uma pessoa.
    """
    # TODO: implementar

@app.get("/pessoas/{id}")               #200, 404
async def retorna_pessoa(id: int):
    """
    Consulta uma pessoa pelo seu id.
    """
    # TODO: implementar

@app.get("/pessoas")
async def busca_pessoas(termo: str):     #200, 400
    """
    Busca por pessoas a partir de um termo de busca.
    """
    # TODO: implementar

@app.get("/contagem-pessoas")
async def conta_pessoas():               #200
    """
    Retorna a contagem de pessoas cadastradas.
    """
    # Implementação não fornecida
'''


