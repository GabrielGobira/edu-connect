-- EduConnect - Migração da tabela usuarios
-- Objetivo: permitir apenas os tipos admin e professor.
-- Faça um backup do banco antes de executar.
-- Execute apenas em bancos que ainda não possuem a restrição.
-- Interrompa a execução caso qualquer comando apresente erro.

SAVEPOINT migracao_usuarios;

CREATE TABLE usuarios_nova (
    id INTEGER NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT ck_usuario_tipo
        CHECK (tipo IN ('admin', 'professor'))
);

INSERT INTO usuarios_nova (id, nome, email, senha, tipo)
SELECT id, nome, email, senha, tipo
FROM usuarios;

DROP TABLE usuarios;

ALTER TABLE usuarios_nova RENAME TO usuarios;

CREATE UNIQUE INDEX ix_usuarios_email
ON usuarios (email);

CREATE INDEX ix_usuarios_id
ON usuarios (id);

RELEASE SAVEPOINT migracao_usuarios;

-- Validações após a migração
PRAGMA integrity_check;
PRAGMA foreign_key_check;