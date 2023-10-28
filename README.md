# Rinha de Backend

Este pequeno projeto foi inspirado pelo desafio proposto na [Rinha de Backend 2023 Q3](https://github.com/zanfranceschi/rinha-de-backend-2023-q3).

Obviamente cheguei atrasado na festa, mas achei interessante decidi fazer minha implementação como exercício.

O foco do desafio não está no desenvolvimento da API em si, mas conseguir o melhor desempenho possível nos testes de estresse usando pouquíssimos recursos (1.5 vCPU e 3GB de RAM). 

O desafio também especifica o deploy via *docker-compose*, com duas instâncias para a API, uma instância para o *load balancer* e outra para o banco de dados (Postgres, MySQL, ou MongoDB).

A especificação completa pode ser encontrada [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md). 

Os testes de estresse podem ser encontrados [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test).

## Tech Stack

- Postgres (banco de dados)
- Nginx (balanceamento de carga)
- Python / FastAPI  (*framework*)
- cachetools (*cache* local)
- Redis (*cache* remoto)

## Execução da Aplicação

A aplicação completa (incluindo todos os componentes) pode ser iniciada da seguinte forma:

```bash
podman-compose -f docker-compose.yml up --build
```

Para terminar a execução:

```bash
podman-compose -f docker-compose.yml down
```

## Execução dos Testes Unitários

Os testes unitários podem ser executados da seguinte forma:

```bash
podman-compose -f docker-compose-tests.yml up --build
```

Para terminar sua execução:

```bash
podman-compose -f docker-compose-tests.yml down
```

## Execução dos Testes de Estresse

Originalmente disponíveis [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test), por motivos de conveniência reproduzimos o conteúdo dos testes na pasta `stress-test`.

O primeiro passo é instalar a ferramenta *gatling* (caso já não esteja disponível), através do script auxiliar. O comando abaixo irá instalar o gatling no diretório `~/bin/gatling-3.9.5`.

```bash
cd stress-test
./install-gatling.sh ~/bin/
```

O passo seguinte é a execução dos testes em si, conforme mostrado. Antes de executar os testes, inicie a aplicação conforme explicado [anteriormente](#execu%C3%A7%C3%A3o-da-aplica%C3%A7%C3%A3o).

```bash
cd stress-test
./run-test.sh ~/bin/gatling-3.9.5/
```

Os resultados, assim como os logs de execução, podem ser encontrados na pasta `stress-test/user-files/results`.

### Resultados

Realizamos a avaliação de nossa implementação na [AWS](https://aws.amazon.com/), de acordo com o proposto no desafio.
A especificação da VM de referência pode ser encontrada [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/misc/lshw-aws).

A VM utilizada foi do tipo *t3a.xlarge*, com 4 vCPUs (Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz),
16Gib de memória e 30Gib de disco (gp3, *encrypted*, 5000 IOPS, 1000MB/s *throughput*).  
Como sistema operacional, utilizamos a AMI Ubuntu Server 22.04 LTS (ami-0fc5d935ebf8bc3bc).

Primeiro, a configuração do ambiente. 

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

(aws)$ sudo apt -y update
(aws)$ sudo apt -y install git podman python3-pip openjdk-8-jdk-headless unzip
(aws)$ sudo pip install podman-compose

(aws)$ sudo mkdir -p /etc/systemd/system/user@.service.d
(aws) $ sudo tee /etc/systemd/system/user@.service.d/delegate.conf << EOM
[Service]
Delegate=memory pids cpu cpuset
EOM
 
(aws)$ sudo reboot
```

A seguir, a execução dos testes. Para isso, precisamos de dois terminais.

No primeiro terminal, rodamos a aplicação. Note que desabilitamos duas vCPUs antes de iniciar o teste, evitando assim o compartilhamento de vCPUs em um mesmo *core*.

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

(aws)$ echo 0 | sudo tee /sys/devices/system/cpu/cpu2/online 
(aws)$ echo 0 | sudo tee /sys/devices/system/cpu/cpu3/online 
(aws)$ cat /proc/cpuinfo | grep 'core id' 
    core id		: 0
    core id		: 1

(aws)$ git clone https://github.com/ramosfabiano/rinha-de-backend-2023-q3.git
(aws)$ cd  rinha-de-backend-2023-q3
(aws)$ podman-compose -f docker-compose.yml up 
```

No segundo terminal, instalamos o gatling e disparamos o teste:

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

(aws)$ cd rinha-de-backend-2023-q3/stress-test/
(aws)$ mkdir -p ~/bin 
(aws)$ ./install-gatling.sh ~/bin/
(aws)$ ./run-test.sh ~/bin/gatling-3.9.5/
```

### Discussão

No que tange à implementação, levamos a cabo as otimizações mais comuns, como caching (local e remoto), uso de
assincronismo, criação de um campo extra na tabela para acelerar as buscas por termo. Tentamos também
manter o código razoavelmente limpo e organizado, e não lançar mão de otimizações inseguras que não seriam feitas
em produção, como por exemplo uso de SQL diretamente. Implementamos também testes unitários para a API.

Outro ponto importante na implementação deste desafio foram a configurações específicas (nível de log, número máximo de conexão,
tamanhos de buffer, etc.) dos serviços postgres, nginx e redis. Focamos em customizar as opções mais relevantes e 
determinamos os valores adequados através de experimentação.

Além disso, a distribuição ideal dos recursos entre os contêineres também foi um ponto crucial. Como metodologia, iniciamos 
com um deployment sem grandes limitações de recursos, de forma que a aplicação conseguisse aguentar o teste de estresse e 
terminar sem falhas com os 46k+ registros no banco.

Uma vez determinada tal configuração, fomos reduzindo invidualmente os recursos do postgres,
do redis e do nginx, nesta ordem, de forma a identificar onde estavam os gargalos e definir as configurações
mínimas (em termos de recursos) e ótimas (em termos de configuração específicas) para cada serviço. 
Realizamos diversas interações deste processo até determinar as melhores configurações possíveis.

Durante o processo, o mínimo de recursos que conseguimos utilizar para uma execução sem falhas foi
2.2 vCPUs e 3.0 GiB de memória. Essa configuração está registrada no `docker-compose-minimum.yml`.

```
================================================================================
---- Global Information --------------------------------------------------------
> request count                                     114952 (OK=114952 KO=0     )
> min response time                                      0 (OK=0      KO=-     )
> max response time                                  30322 (OK=30322  KO=-     )
> mean response time                                  4770 (OK=4770   KO=-     )
> std deviation                                       6876 (OK=6876   KO=-     )
> response time 50th percentile                       1050 (OK=1049   KO=-     )
> response time 75th percentile                       7171 (OK=7177   KO=-     )
> response time 95th percentile                      20274 (OK=20273  KO=-     )
> response time 99th percentile                      23716 (OK=23716  KO=-     )
> mean requests/sec                                495.483 (OK=495.483 KO=-     )
---- Response Time Distribution ------------------------------------------------
> t < 800 ms                                         53480 ( 47%)
> 800 ms <= t < 1200 ms                              10405 (  9%)
> t >= 1200 ms                                       51067 ( 44%)
> failed                                                 0 (  0%)
================================================================================
...
46559
```