-- Criação do banco de dados, caso ele ainda não exista
CREATE DATABASE supermario;

-- Conecta ao banco supermario
\c supermario;

-- Criação das tabelas

CREATE TABLE Item (
    idItem SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    efeito VARCHAR(50),
    duração INTEGER,
    raridade VARCHAR(20),
    CONSTRAINT item_pk PRIMARY KEY (idItem)
);

CREATE TABLE Yoshi (
    idYoshi SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    CONSTRAINT yoshi_pk PRIMARY KEY (idYoshi)
);

CREATE TABLE Moeda (
    idMoeda SERIAL NOT NULL,
    valor INTEGER NOT NULL,
    CONSTRAINT moeda_pk PRIMARY KEY (idMoeda)
);

CREATE TABLE Mundo (
    idMundo SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descrição TEXT,
    nivel INTEGER NOT NULL,
    CONSTRAINT mundo_pk PRIMARY KEY (idMundo)
);

CREATE TABLE Bloco (
    idBloco SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    idItem INTEGER,
    idYoshi INTEGER,
    idMoeda INTEGER,
    CONSTRAINT bloco_pk PRIMARY KEY (idBloco),
    FOREIGN KEY (idItem) REFERENCES Item(idItem) ON DELETE SET NULL,
    FOREIGN KEY (idYoshi) REFERENCES Yoshi(idYoshi) ON DELETE SET NULL,
    FOREIGN KEY (idMoeda) REFERENCES Moeda(idMoeda) ON DELETE SET NULL  
);

CREATE TABLE Fase (
    idFase SERIAL NOT NULL,
    nome VARCHAR(15) NOT NULL,
    nivel INTEGER NOT NULL,
    idMundo INTEGER NOT NULL,
    CONSTRAINT fase_pk PRIMARY KEY (idFase),
    FOREIGN KEY (idMundo) REFERENCES Mundo(idMundo)
);

CREATE TABLE Checkpoint (
    idCheckpoint SERIAL NOT NULL,
    pontuação INTEGER NOT NULL,
    CONSTRAINT checkpoint_pk PRIMARY KEY (idCheckpoint)
);

CREATE TABLE Loja (
    idLoja SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    CONSTRAINT loja_pk PRIMARY KEY (idLoja)
);

CREATE TABLE Local (
    idLocal SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
    descricao TEXT,
    idFase INTEGER NOT NULL,
    idBloco INTEGER,
    idPersonagem INTEGER,
    idLoja INTEGER,
    idCheckpoint INTEGER,
    CONSTRAINT local_pk PRIMARY KEY (idLocal),
    FOREIGN KEY (idFase) REFERENCES Fase(idFase),
    FOREIGN KEY (idBloco) REFERENCES Bloco(idBloco) ON DELETE SET NULL,
    FOREIGN KEY (idLoja) REFERENCES Loja(idLoja) ON DELETE SET NULL,
    FOREIGN KEY (idCheckpoint) REFERENCES Checkpoint(idCheckpoint) ON DELETE SET NULL
);

CREATE TABLE Personagem (
    idPersonagem SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    vida INTEGER NOT NULL,
    dano INTEGER NOT NULL,
    pontos INTEGER NOT NULL,
    idLocal INTEGER, -- Removendo o NOT NULL
    tipoJogador VARCHAR(15), -- "Jogador", "Inimigo", "NPC"
    CONSTRAINT personagem_pk PRIMARY KEY (idPersonagem),
    FOREIGN KEY (idLocal) REFERENCES Local(idLocal)
);

CREATE TABLE Inimigo (
    idPersonagem INTEGER NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    habilidade VARCHAR(15) NOT NULL,
    CONSTRAINT inimigo_pk PRIMARY KEY (idPersonagem),
    FOREIGN KEY (idPersonagem) REFERENCES Personagem(idPersonagem)
);

CREATE TABLE Inventario (
    idInventario SERIAL NOT NULL,
    quantidade INTEGER NOT NULL,
    idItem INTEGER NOT NULL,
    idPersonagem INTEGER NOT NULL,
    CONSTRAINT inventario_pk PRIMARY KEY (idInventario),
    FOREIGN KEY (idItem) REFERENCES Item(idItem),
    FOREIGN KEY (idPersonagem) REFERENCES personagem(idpersonagem)
);


CREATE TABLE Jogador (
    idPersonagem SERIAL NOT NULL,
    moeda INTEGER,
    idInventario INTEGER NOT NULL,
    idYoshi INTEGER,
    CONSTRAINT jogador_pk PRIMARY KEY (idPersonagem),
    FOREIGN KEY (idPersonagem) REFERENCES Personagem(idPersonagem),
    FOREIGN KEY (idInventario) REFERENCES Inventario(idInventario),
    FOREIGN KEY (idYoshi) REFERENCES Yoshi(idYoshi)
);

CREATE TABLE Instancia (
    idInstancia SERIAL NOT NULL,
    vidaAtual INTEGER NOT NULL,
    moedaAtual INTEGER NOT NULL, 
    idJogador INTEGER NOT NULL,
    CONSTRAINT instancia_pk PRIMARY KEY (idInstancia)
);

