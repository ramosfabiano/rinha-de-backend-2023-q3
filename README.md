# Rinha de Backend

Este pequeno projeto foi inspirado pelo desafio proposto na [Rinha de Backend 2023 Q3](https://github.com/zanfranceschi/rinha-de-backend-2023-q3).

Obviamente cheguei atrasado na festa, mas achei interessante decidi fazer minha implementação como exercício.

O foco do desafio não está no desenvolvimento da API em si, mas conseguir o melhor desempenho possível nos testes de estresse usando pouquíssimos recursos (1.5 vCPU e 3GB de RAM). 

O desafio também especifica o deploy via *docker-compose*, com duas instâncias para a API, uma instância para o *load balancer* e outra para o banco de dados (Postgres, MySQL, ou MongoDB).

A especificação completa pode ser encontrada [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md). 

Os testes de estresse podem ser encontrados [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test).

## Tech Stack

- Postgres
- Python / FastAPI
- Nginx
- Redis

## Execução

A aplicação completa (incluindo todos os componentes) pode ser iniciada da seguinte forma:

```
podman-compose build
podman-compose up
```

Para terminar sua execução:

```
podman-compose down
```

## Execução dos unit tests

Os testes unitários podem ser executados da seguinte forma:

```
podman-compose -f docker-compose-tests.yml build
podman-compose -f docker-compose-tests.yml up
```

Para terminar sua execução:

```
podman-compose -f docker-compose-tests.yml down
```

## Implementação

### Banco de Dados

Utilizamos o *Postgres* como banco de dados, a partir da imagem padrão `docker.io/postgres`.  Vale a pena destacar as configurações customizadas presentes em `postgres/config.sql`.
Os valores utilizados aqui foram determinados baseados em experimentação.

### API

Implementamos a API em python, utilizando o *framework* FastAPI.

### Balanceamento de Carga


### Caching


## Resultados



