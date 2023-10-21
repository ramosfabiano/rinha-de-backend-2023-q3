CREATE TABLE IF NOT EXISTS pessoas (
    id VARCHAR(36),
    apelido VARCHAR(32) CONSTRAINT APELIDO_PK PRIMARY KEY,
    nome VARCHAR(128),
    nascimento CHAR(10),
    stack VARCHAR(2048)
);

