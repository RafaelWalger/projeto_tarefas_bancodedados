-- =====================================================================
-- Sistema de Gerenciamento de Tarefas (Oracle SQL)
-- Somente criacao de sequences e tabelas (nao insere dados).
-- IMPORTANTE: nao ha linhas em branco DENTRO dos comandos, porque o
-- DBeaver usa linha em branco como separador de comando.
-- =====================================================================

-- (OPCIONAL) Para recriar do zero, apague o "-- " das 6 linhas abaixo,
-- selecione SO elas e execute com Alt+X. Depois comente de novo.
-- Erros de "does not exist" nessa etapa sao normais.
-- ATENCAO: apaga todos os dados.
-- DROP TABLE tarefa CASCADE CONSTRAINTS;
-- DROP TABLE categoria CASCADE CONSTRAINTS;
-- DROP TABLE usuario CASCADE CONSTRAINTS;
-- DROP SEQUENCE seq_tarefa;
-- DROP SEQUENCE seq_categoria;
-- DROP SEQUENCE seq_usuario;

-- ---------------------------------------------------------------------
-- SEQUENCES (geram as chaves primarias)
-- ---------------------------------------------------------------------
CREATE SEQUENCE seq_usuario START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_categoria START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_tarefa START WITH 1 INCREMENT BY 1 NOCACHE;

-- ---------------------------------------------------------------------
-- USUARIO
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
    id_usuario NUMBER(10) NOT NULL,
    nome VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    cargo VARCHAR2(50),
    CONSTRAINT pk_usuario PRIMARY KEY (id_usuario),
    CONSTRAINT uq_usuario_email UNIQUE (email)
);

-- ---------------------------------------------------------------------
-- CATEGORIA
-- ---------------------------------------------------------------------
CREATE TABLE categoria (
    id_categoria NUMBER(10) NOT NULL,
    nome VARCHAR2(50) NOT NULL,
    descricao VARCHAR2(200),
    CONSTRAINT pk_categoria PRIMARY KEY (id_categoria)
);

-- ---------------------------------------------------------------------
-- TAREFA (tabela filha: referencia USUARIO e CATEGORIA)
-- Sem ON DELETE: o padrao do Oracle ja impede apagar usuario/categoria
-- que tenham tarefas (erro ORA-02292); o programa trata esse erro.
-- ---------------------------------------------------------------------
CREATE TABLE tarefa (
    id_tarefa NUMBER(10) NOT NULL,
    titulo VARCHAR2(150) NOT NULL,
    descricao VARCHAR2(500),
    status VARCHAR2(20) DEFAULT 'Pendente' NOT NULL,
    prioridade VARCHAR2(10) DEFAULT 'Media' NOT NULL,
    data_criacao DATE NOT NULL,
    data_conclusao DATE,
    horas_gastas NUMBER(6,2) DEFAULT 0 NOT NULL,
    id_usuario NUMBER(10) NOT NULL,
    id_categoria NUMBER(10) NOT NULL,
    CONSTRAINT pk_tarefa PRIMARY KEY (id_tarefa),
    CONSTRAINT fk_tarefa_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    CONSTRAINT fk_tarefa_categoria FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
    CONSTRAINT ck_tarefa_status CHECK (status IN ('Pendente', 'Em andamento', 'Concluida')),
    CONSTRAINT ck_tarefa_prioridade CHECK (prioridade IN ('Baixa', 'Media', 'Alta')),
    CONSTRAINT ck_tarefa_horas CHECK (horas_gastas >= 0),
    CONSTRAINT ck_tarefa_datas CHECK (data_conclusao IS NULL OR data_conclusao >= data_criacao)
);
