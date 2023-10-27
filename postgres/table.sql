CREATE TABLE IF NOT EXISTS pessoas (
    id VARCHAR(36) CONSTRAINT APELIDO_PK PRIMARY KEY,
    apelido VARCHAR(32) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    nascimento CHAR(10) NOT NULL,
    stack VARCHAR(2048),
    termo VARCHAR GENERATED ALWAYS AS (LOWER(apelido || ' ' || nome || COALESCE(' (' || stack || ')', ''))) STORED
);