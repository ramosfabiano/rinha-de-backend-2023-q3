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

## Requisitos

Desenvolvemos nossa solução na plataforma Ubuntu Linux 22.04 LTS, gerenciamento e execução de *containers* realizado através do *podman* 3.4.4 e do *podman-compose* 1.0.6.

A instalação e configuração do *podman* e do *podman-compose* pode ser feita da seguinte forma:

```bash
# instala o podman
sudo apt -y update
sudo apt -y install podman

# instala o podman-compose
sudo apt -y install python3-pip
pip install podman-compose

# configura o podman para permitir o limite de cpus
sudo mkdir -p /etc/systemd/system/user@.service.d
sudo tee /etc/systemd/system/user@.service.d/delegate.conf << EOM
[Service]
Delegate=memory pids cpu cpuset
EOM

# reinicia o sistema para que a configuração tenha efeito
sudo reboot
```

As demais dependências são *git*, *unzip* e *openjdk*, que podem ser instaladas assim:

```bash
sudo apt -y install git unzip openjdk-11-jdk
```

Por último, recomendamos desabilitar o uso de *hyperthreading*, para que a limitação de CPU definida aos *containers* seja verdadeira e determinística.


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

## Avaliação (AWS EC2)

Realizamos a avaliação de nossa implementação na [AWS EC2](https://aws.amazon.com/), conforme proposto no desafio.

A VM utilizada foi do tipo *c5d.xlarge*, com 4 vCPUs (Intel(R) Xeon(R) Platinum 8275CL CPU @ 3.00GHz) e 8 Gib de memória. A instância inclui um disco SSD local de 100GB.

Como sistema operacional, utilizamos a AMI Ubuntu Server 22.04 LTS (ami-0fc5d935ebf8bc3bc) para replicar nosso ambiente de desenvolvimento local.

Primeiro, a configuração do ambiente. 

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

# podman
(aws)$ sudo apt -y update
(aws)$ sudo apt -y install git podman python3-pip openjdk-11-jdk-headless unzip
(aws)$ sudo pip install podman-compose

# configura podman para permitir controlar uso parcial de recursos
(aws)$ sudo mkdir -p /etc/systemd/system/user@.service.d
(aws)$ sudo tee /etc/systemd/system/user@.service.d/delegate.conf << EOM
[Service]
Delegate=memory pids cpu cpuset
EOM

# configura podman para armazenar imagens e overlays no SSD que montaremos à frente
(aws)$ sudo tee /etc/containers/storage.conf << EOM
[storage]
driver = "overlay"
rootless_storage_path = "/mnt/storage"
EOM

(aws)$ sudo reboot
```

A seguir, a execução dos testes. Para isso, precisamos de dois terminais.

No primeiro terminal, configuramos o sistema e rodamos a aplicação. Note preparamos o disco local SSD, que é efêmero (não retém seu conteúdo ou configuração após um boot).

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

# configura o SSD. Não sobrevive a reboots.
(aws) $ sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/nvme1n1
(aws) $ sudo mount /dev/nvme1n1 /mnt
(aws) $ sudo chown ubuntu.ubuntu /mnt/

# executa a aplicação
(aws)$ cd /mnt
(aws)$ git clone https://github.com/ramosfabiano/rinha-de-backend-2023-q3.git
(aws)$ cd rinha-de-backend-2023-q3
(aws)$ podman-compose -f docker-compose.yml up --build 
```

No segundo terminal, instalamos o gatling e disparamos o teste:

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

(aws)$ cd /mnt/rinha-de-backend-2023-q3/stress-test/

# instala o gatling
(aws)$ ./install-gatling.sh ~/mnt/

# roda o teste
(aws)$ time ./run-test.sh ~/mnt/gatling-3.9.5/
```

### Resultados

Apresentamos aqui os resultados...

### Discussão

- determinismo da avaliação: hyperthreading, EBS vs disco local
  - assumimos que a máquina host possui pelo menos 2 cores (cpuset 0 e 1)

- requests podem falhar?

- modelo de consistência da API

No que tange à implementação, levamos a cabo as otimizações mais comuns, como caching (local e remoto), uso de
assincronismo, criação de um campo extra na tabela para acelerar as buscas por termo. Tentamos também
manter o código razoavelmente limpo e organizado, e não lançar mão de otimizações inseguras que não seriam feitas
em produção, como por exemplo uso de SQL diretamente. Implementamos também testes unitários para a API.

Outro ponto importante na implementação deste desafio foram a configurações específicas dos serviços postgres, nginx e redis
 (nível de log, número máximo de conexão, tamanhos de buffer, etc...), Focamos em customizar as opções mais relevantes e 
determinamos os valores adequados através de pesquisa seguida de experimentação.

Além disso, a distribuição ideal dos recursos entre os contêineres também foi um ponto crucial. Como metodologia, iniciamos 
com uma composição com recursos abuntantes para cada unidade, de forma que a aplicação conseguisse aguentar o teste de estresse e 
terminar sem falhas. Uma vez determinada tal configuração, fomos reduzindo invidualmente os recursos do postgres,
do redis e do nginx, nesta ordem, de forma a identificar onde estavam os gargalos e definir as configurações
mínimas (em termos de recursos) e ótimas (em termos de configuração específicas) para cada serviço. 
Realizamos diversas interações deste processo até determinar as melhores configurações possíveis.

