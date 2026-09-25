-- Script de inicialização automática do banco de dados
-- Este arquivo é executado automaticamente pelo container do PostgreSQL na primeira inicialização
-- através do diretório /docker-entrypoint-initdb.d/

CREATE TABLE IF NOT EXISTS objetos_perdidos (
    id_objeto SERIAL PRIMARY KEY,
    nome_objeto VARCHAR(255) NOT NULL,
    cor VARCHAR(100) NOT NULL,
    data_perdido VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS objetos_achados (
    id_objetoA SERIAL PRIMARY KEY,
    nome_objeto_achado VARCHAR(255) NOT NULL,
    cor_achado VARCHAR(100) NOT NULL,
    nome_pessoa VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    contato VARCHAR(200) NOT NULL
);
