# Rinha de Backend

Este pequeno projeto foi inspirado pelo desafio proposto na [Rinha de Backend 2023 Q3](https://github.com/zanfranceschi/rinha-de-backend-2023-q3).

Obviamente cheguei atrasado na festa, mas achei interessante decidi fazer minha implementação como exercício.

O foco do desafio não está no desenvolvimento da API em si, mas conseguir o melhor desempenho possível nos testes de estresse usando pouquíssimos recursos (1.5 vCPU e 3GB de RAM). 

O desafio também especifica o deploy via *docker-compose*, com duas instâncias para a API, uma instância para o *load balancer* e outra para o banco de dados (Postgres, MySQL, ou MongoDB).

A especificação completa pode ser encontrada [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md). 

Os testes de estresse podem ser encontrados [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test).

## Tech Stack

- Postgres (banco de dados)
- Python / FastAPI  (*framework*)
- Nginx (balanceamento de carga)
- Redis (*caching*)

## Execução da Aplicação

A aplicação completa (incluindo todos os componentes) pode ser iniciada da seguinte forma:

```
podman-compose build
podman-compose up
```

Para terminar sua execução:

```
podman-compose down
```

## Execução dos Testes Unitários

Os testes unitários podem ser executados da seguinte forma:

```
podman-compose -f docker-compose-tests.yml build
podman-compose -f docker-compose-tests.yml up
```

Para terminar sua execução:

```
podman-compose -f docker-compose-tests.yml down
```

## Execução dos Testes de Estresse

Originalmente disponíveis [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test), por motivos de conveniência reproduzimos o conteúdo dos testes na pasta `stress-test`.

O primeiro passo é instalar a ferramenta *gatling* (caso já não esteja disponível), através do script auxiliar. O comando abaixo irá instalar o gatling no diretório `~/bin/gatling-3.9.5`.

```
cd stress-test
./install-gatling.sh ~/bin/
```

O passo seguinte é a execução dos testes em si, conforme mostrado. Antes de executar os testes, inicie a aplicação conforme explicado [anteriormente](##execu%C3%A7%C3%A3o-da-aplica%C3%A7%C3%A3o).

```
cd stress-test
./run-test.sh ~/bin/gatling-3.9.5/
```

Os resultados, assim como os logs de execução, podem ser encontrados na pasta `stress-test/user-files/results`.

### Resultados



