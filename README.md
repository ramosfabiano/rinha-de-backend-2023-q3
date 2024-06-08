# Rinha de Backend

Este pequeno projeto foi inspirado pelo desafio proposto na [Rinha de Backend 2023 Q3](https://github.com/zanfranceschi/rinha-de-backend-2023-q3).

Chegamos tarde para a festa, mas como a idéia era bastante interessante, decidimos fazer a implementação como exercício.

Em resumo, o objetivo é implementar uma API simples, capaz de sobreviver a um teste de estresse usando pouquíssimos recursos (1.5 vCPU e 3GB de RAM).

A especificação completa pode ser encontrada [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md). 

## Tech Stack

- Postgres (banco de dados)
- Nginx (balanceamento de carga)
- Python / FastAPI  (*framework* de desenvolvimento)
- Cachetools (*cache* local)
- Redis (*cache* remoto)

## Requisitos

Desenvolvemos nossa solução sobre a plataforma Ubuntu Linux 22.04 LTS, com gerenciamento e execução de contêineres realizado através do *podman* e do *podman-compose*.

A instalação e configuração do *podman* e do *podman-compose* pode ser feita da seguinte forma:

```bash
# instala o podman
$ sudo apt -y update
$ sudo apt -y install podman

# instala o podman-compose
$ sudo apt -y install python3-pip
$ pip install podman-compose

$ podman-compose --version
podman-compose version: 1.0.6
['podman', '--version', '']
using podman version: 3.4.4
podman-compose version 1.0.6
podman --version 
podman version 3.4.4

# configura os recursos que o podman pode gerenciar
$ sudo mkdir -p /etc/systemd/system/user@.service.d
$ sudo tee /etc/systemd/system/user@.service.d/delegate.conf << EOM
[Service]
Delegate=memory pids cpu cpuset
EOM

# reinicia o sistema para que a configuração tenha efeito
$ sudo reboot
```

As demais dependências são *git*, *unzip* e *openjdk*, que podem ser instaladas assim:

```bash
$ sudo apt -y install git unzip openjdk-11-jdk
```

## Execução da Aplicação

A aplicação completa (incluindo todos os componentes) pode ser iniciada da seguinte forma:

```bash
$ podman-compose -f docker-compose.yml up --build
```

Para terminar a execução:

```bash
$ podman-compose -f docker-compose.yml down
```

## Execução dos Testes Unitários

Os testes unitários podem ser executados da seguinte forma:

```bash
$ podman-compose -f docker-compose-tests.yml up --build
```

Para terminar sua execução:

```bash
$ podman-compose -f docker-compose-tests.yml down
```

## Execução dos Testes de Estresse

Originalmente disponíveis [aqui](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/tree/main/stress-test), por motivos de conveniência reproduzimos o conteúdo dos testes de estresse na pasta `stress-test`.

Para a execução dos testes, o primeiro passo é instalar a ferramenta *gatling* (caso já não esteja disponível), através do *script* auxiliar. O comando abaixo irá instalar o *gatling* no diretório `~/bin/gatling-3.9.5`.

```bash
$ cd stress-test
$ ./install-gatling.sh ~/bin/
```

O passo seguinte é a execução dos testes em si, conforme mostrado. Antes de executar os testes, inicie a aplicação conforme explicado anteriormente.

```bash
$ cd stress-test
$ ./run-test.sh ~/bin/gatling-3.9.5/
```

Após o término dos testes, os resultados poderão ser encontrados na pasta `stress-test/user-files/results`.

## Avaliação - AWS EC2

Realizamos a avaliação de nossa implementação na [AWS EC2](https://aws.amazon.com/), conforme proposto no desafio.

A VM utilizada foi do tipo *c5d.2xlarge*, com 8 vCPUs, 16 Gib de memória, e disco SSD local. Como sistema operacional, utilizamos a AMI Ubuntu Server 22.04 LTS (ami-0fc5d935ebf8bc3bc).

Nossa motivação para estas escolhas foi tentar replicar ao máximo nosso ambiente de desenvolvimento local para evitar um novo ciclo de refinamento da distribuição de recursos.

```bash
(aws) $ sudo lshw -short -sanitize -notime -c system,bus,memory,processor,bridge,storage,disk,volume,network

H/W path      Device           Class          Description
=========================================================
                               system         c5d.xlarge
/0                             bus            Motherboard
/0/0                           memory         64KiB BIOS
/0/4                           processor      Intel(R) Xeon(R) Platinum 8275CL CPU @ 3.00GHz
/0/4/5                         memory         1536KiB L1 cache
/0/4/6                         memory         24MiB L2 cache
/0/4/7                         memory         35MiB L3 cache
/0/8                           memory         8GiB System Memory
/0/8/0                         memory         8GiB DIMM DDR4 Static column Pseudo-static Synchronous Window DRAM 2933 MH
/0/100                         bridge         440FX - 82441FX PMC [Natoma]
/0/100/1                       bridge         82371SB PIIX3 ISA [Natoma/Triton II]
/0/100/1/0                     system         PnP device PNP0b00
/0/100/4      /dev/nvme0       storage        Amazon Elastic Block Store
/0/100/4/0    hwmon1           disk           NVMe disk
/0/100/4/2    /dev/ng0n1       disk           NVMe disk
/0/100/4/1    /dev/nvme0n1     disk           8589MB NVMe disk
/0/100/4/1/1  /dev/nvme0n1p1   volume         8080MiB EXT4 volume
/0/100/4/1/e  /dev/nvme0n1p14  volume         4095KiB BIOS Boot partition
/0/100/4/1/f  /dev/nvme0n1p15  volume         105MiB Windows FAT volume
/0/100/5      ens5             network        Elastic Network Adapter (ENA)
/0/100/1f     /dev/nvme1       storage        Amazon EC2 NVMe Instance Storage
/0/100/1f/0   hwmon0           disk           NVMe disk
/0/100/1f/2   /dev/ng1n1       disk           NVMe disk
/0/100/1f/1   /dev/nvme1n1     disk           100GB NVMe disk
```

Primeiro, a configuração do ambiente. 

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

# podman
(aws)$ sudo apt -y update
(aws)$ sudo apt -y install git podman python3-pip openjdk-11-jdk-headless unzip
(aws)$ sudo pip install podman-compose

# configura os recursos que o podman pode gerenciar
(aws)$ sudo mkdir -p /etc/systemd/system/user@.service.d
(aws)$ sudo tee /etc/systemd/system/user@.service.d/delegate.conf << EOM
[Service]
Delegate=memory pids cpu cpuset
EOM

# configura podman para armazenar imagens e overlays no SSD que montaremos a seguir
(aws)$ sudo tee /etc/containers/storage.conf << EOM
[storage]
driver = "overlay"
rootless_storage_path = "/mnt/storage"
EOM

(aws)$ sudo reboot
```

A seguir, a execução dos testes. Para isso, precisamos de dois terminais.

No primeiro terminal, configuramos o sistema e rodamos a aplicação. Note que preparamos o disco local SSD, que é efêmero (não retém seu conteúdo ou configuração após um *reboot*).
Desabilitamos também o SMT neste momento.

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

# configura o SSD. Não sobrevive a reboots.
(aws) $ sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/nvme1n1
(aws) $ sudo mount /dev/nvme1n1 /mnt
(aws) $ sudo chown ubuntu.ubuntu /mnt/

# desabilita SMT. Não sobrevive a reboots.
(aws)$ echo 0 | sudo tee /sys/devices/system/cpu/cpu{4,5,6,7}/online 
(aws)$ cat /proc/cpuinfo | grep 'core id' 
core id		: 0
core id		: 1
core id		: 2
core id		: 3

# executa a aplicação
(aws)$ cd /mnt
(aws)$ git clone https://github.com/ramosfabiano/rinha-de-backend-2023-q3.git
(aws)$ cd rinha-de-backend-2023-q3
(aws)$ podman-compose -f docker-compose.yml up --build 
```

No segundo terminal, instalamos o *gatling* e disparamos o teste:

```bash
$ ssh -i <chave_privada> ubuntu@<ip_publico_vm>

(aws)$ cd /mnt/rinha-de-backend-2023-q3/stress-test/

# instala o gatling
(aws)$ ./install-gatling.sh /mnt/

# roda o teste
(aws)$ time ./run-test.sh /mnt/gatling-3.9.5/
```

### Resultados - AWS EC2

Apresentamos aqui os resultados da execução de nossa aplicação na AWS EC2.

![resumo-texto](https://github.com/ramosfabiano/rinha-de-backend-2023-q3/blob/main/resultados-ec2/resumo-texto.png)

![resumo](https://github.com/ramosfabiano/rinha-de-backend-2023-q3/blob/main/resultados-ec2/resumo.png)

![grafico1](https://github.com/ramosfabiano/rinha-de-backend-2023-q3/blob/main/resultados-ec2/performance.png)

Conseguimos uma execução sem falhas, indicando que nossas soluções de otimização e refinamento da configuração dos serviços foi bem sucedida.

Como referẽncia, um total de 46583 registros se encontravam persistidos no banco após a finalização dos testes.
Esse número deve ser interpretado cuidadosamente se comparado aos resultados dos participantes do desafio, pois o
ambiente e condições de execução foi muito provavelmente distinto. No entanto, é uma confirmação de que nosso esforço
foi eficaz e na direção correta.
