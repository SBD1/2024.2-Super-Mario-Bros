-- Criação do banco de dados, caso ele ainda não exista
CREATE DATABASE supermario;

-- Conecta ao banco supermario
\c supermario;

-- Criação das tabelas
CREATE TABLE IF NOT EXISTS Yoshi (
    idYoshi SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    idBloco INTEGER NOT NULL,
    CONSTRAINT yoshi_pk PRIMARY KEY (idYoshi)
);

CREATE TABLE IF NOT EXISTS Bloco (
    idBloco SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    idLocal INTEGER NOT NULL,
    CONSTRAINT bloco_pk PRIMARY KEY (idBloco)
);

CREATE TABLE IF NOT EXISTS Cano (
    idCano SERIAL NOT NULL,
    idDestino VARCHAR(35) NOT NULL,
    CONSTRAINT cano_pk PRIMARY KEY (idCano)
);

CREATE TABLE IF NOT EXISTS Mundo (
    idMundo SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descrição TEXT,
    nivel INTEGER NOT NULL,
    CONSTRAINT mundo_pk PRIMARY KEY (idMundo),
    FOREIGN KEY (idMundo) REFERENCES Cano(idCano)
);

CREATE TABLE IF NOT EXISTS Fase (
    idFase SERIAL NOT NULL,
    nome VARCHAR(15) NOT NULL,
    nivel INTEGER NOT NULL,
    idMundo INTEGER NOT NULL,
    CONSTRAINT fase_pk PRIMARY KEY (idFase),
    FOREIGN KEY (idMundo) REFERENCES Mundo(idMundo)
);

CREATE TABLE IF NOT EXISTS Inventário (
    idIventário SERIAL NOT NULL,
    quantidade INTEGER NOT NULL,
    idJogador INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    CONSTRAINT inventário_pk PRIMARY KEY (idIventário)
);

CREATE TABLE IF NOT EXISTS Inimigo (
    idInimigo SERIAL NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    CONSTRAINT inimigo_pk PRIMARY KEY (idInimigo)
);

CREATE TABLE IF NOT EXISTS Moeda (
    idMoeda SERIAL NOT NULL,
    valor INTEGER NOT NULL,
    idBloco INTEGER NOT NULL,
    CONSTRAINT moeda_pk PRIMARY KEY (idMoeda),
    FOREIGN KEY (idBloco) REFERENCES Bloco(idBloco)
);

CREATE TABLE IF NOT EXISTS Loja (
    idLoja SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    idLocal INTEGER NOT NULL,
    CONSTRAINT loja_pk PRIMARY KEY (idLoja)
);

CREATE TABLE IF NOT EXISTS Item (
    idItem SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    efeito VARCHAR(50),
    duração INTEGER,
    raridade VARCHAR(20),
    idBloco INTEGER NOT NULL,
    CONSTRAINT item_pk PRIMARY KEY (idItem),
    FOREIGN KEY (idBloco) REFERENCES Bloco(idBloco)
);

CREATE TABLE IF NOT EXISTS Personagem (
    idPersonagem SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    vida INTEGER NOT NULL,
    dano INTEGER NOT NULL,
    pontos INTEGER NOT NULL,
    idLocal INTEGER NOT NULL,
    CONSTRAINT personagem_pk PRIMARY KEY (idPersonagem),
    FOREIGN KEY (idLocal) REFERENCES Local(idLocal)
);

CREATE TABLE IF NOT EXISTS Local (
    idLocal SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    idFase INTEGER NOT NULL,
    CONSTRAINT local_pk PRIMARY KEY (idLocal),
    FOREIGN KEY (idFase) REFERENCES Fase(idFase)
);

CREATE TABLE IF NOT EXISTS Checkpoint (
    idCheckpoint SERIAL NOT NULL,
    pontuação INTEGER NOT NULL,
    idLocal INTEGER NOT NULL,
    CONSTRAINT checkpoint_pk PRIMARY KEY (idCheckpoint)
);

CREATE TABLE IF NOT EXISTS Jogador (
    idJogador SERIAL NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    moeda INTEGER NOT NULL,
    idItem INTEGER,
    idYoshi INTEGER,
    CONSTRAINT jogador_pk PRIMARY KEY (idJogador),
    FOREIGN KEY (idItem) REFERENCES Inventário(IdItem),
    FOREIGN KEY (idYoshi) REFERENCES Yoshi(idYoshi)
);

CREATE TABLE IF NOT EXISTS Instancia (
    idInstancia SERIAL NOT NULL,
    vidaAtual INTEGER NOT NULL,
    moedaAtual INTEGER NOT NULL,
    idJogador INTEGER NOT NULL,
    CONSTRAINT instancia_pk PRIMARY KEY (idInstancia)
);