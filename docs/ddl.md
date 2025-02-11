## Introdução

O DDL (Data Definition Language) é uma parte essencial do SQL (Structured Query Language), responsável pela definição da estrutura de um banco de dados.

Com a DDL, é possível criar, alterar e excluir objetos no banco de dados, como tabelas, índices, esquemas, visões e outros elementos relacionados à organização dos dados.

Por meio dela, desenvolvedores e administradores podem configurar a estrutura base que será utilizada para armazenar e gerenciar informações, garantindo uma organização eficiente e flexível para os sistemas que utilizam bancos de dados relacionais.

## Descrição das Tabelas e Entidades

### Yoshi

A tabela **Yoshi** armazena informações sobre a entidade Yoshi no sistema.

```sql
CREATE TABLE Yoshi (
    idYoshi SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    CONSTRAINT yoshi_pk PRIMARY KEY (idYoshi)
);
```

**Colunas:**

- `idYoshi`: Identificador único de Yoshi (chave primária).
- `nome`: Nome de Yoshi.

### Bloco

A tabela **Bloco** armazena detalhes sobre os blocos existentes no jogo.

```sql
CREATE TABLE Bloco (
    idBloco SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    idItem INTEGER,
    idYoshi INTEGER,
    idMoeda INTEGER,
    idFase INTEGER, -- Removendo o NOT NULL
    CONSTRAINT bloco_pk PRIMARY KEY (idBloco),
    FOREIGN KEY (idItem) REFERENCES Item(idItem) ON DELETE SET NULL,
    FOREIGN KEY (idYoshi) REFERENCES Yoshi(idYoshi) ON DELETE SET NULL,
    FOREIGN KEY (idMoeda) REFERENCES Moeda(idMoeda) ON DELETE SET NULL,
    FOREIGN KEY (idFase) REFERENCES Fase(idFase)
);
```

**Colunas:**

- `idBloco`: Identificador único do bloco (chave primária).
- `tipo`: Tipo do bloco.
- `idItem`: Referência ao item relacionado ao bloco.
- `idYoshi`: Referência ao yoshi relacionado ao bloco.
- `idMoeda`: Referência ao moeda relacionado ao bloco.
- `idFase`: Referência ao fase relacionado ao bloco.

### Mundo

A tabela **Mundo** armazena informações sobre os mundos disponíveis no jogo.

```sql
CREATE TABLE Mundo (
    idMundo SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    idLoja INTEGER NOT NULL,
    descrição TEXT,
    nivel INTEGER NOT NULL,
    CONSTRAINT mundo_pk PRIMARY KEY (idMundo),
    CONSTRAINT loja_item_loja_fk FOREIGN KEY (idLoja) REFERENCES Loja(idLoja) ON DELETE CASCADE
);

```

**Colunas:**

- `idMundo`: Identificador único do mundo (chave primária).
- `nome`: Nome do mundo.
- `descrição`: Detalhes descritivos sobre o mundo.
- `nivel`: Nível associado ao mundo.
- `idLoja`: Referência a loja associado.

### Fase

A tabela **Fase** organiza os estágios do jogo.

```sql
CREATE TABLE Fase (
    idFase SERIAL NOT NULL,
    nome VARCHAR(15) NOT NULL,
    nivel INTEGER NOT NULL,
    idMundo INTEGER NOT NULL,
    CONSTRAINT fase_pk PRIMARY KEY (idFase),
    FOREIGN KEY (idMundo) REFERENCES Mundo(idMundo)
);
```

**Colunas:**

- `idFase`: Identificador único da fase (chave primária).
- `nome`: Nome da fase.
- `nivel`: Nível da fase.
- `idMundo`: Referência ao mundo ao qual a fase pertence.

### Inventário

A tabela **Inventário** armazena informações sobre os itens em posse do jogador.

```sql
CREATE TABLE Inventario (
    idInventario SERIAL NOT NULL,
    quantidade INTEGER NOT NULL,
    idItem INTEGER NOT NULL,
    idPersonagem INTEGER NOT NULL,
    CONSTRAINT inventario_pk PRIMARY KEY (idInventario),
    FOREIGN KEY (idItem) REFERENCES Item(idItem),
    FOREIGN KEY (idPersonagem) REFERENCES personagem(idpersonagem)
);
```

**Colunas:**

- `idIventário`: Identificador único do inventário (chave primária).
- `quantidade`: Quantidade de itens.
- `IdItem`: Referência ao item.
- `idPersonagem`: Referência ao personagem.

### Inimigo

A tabela **Inimigo** registra detalhes sobre os inimigos no jogo.

```sql
CREATE TABLE Inimigo (
    idInimigo SERIAL NOT NULL,
    idPersonagem INTEGER NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    habilidade VARCHAR(15) NOT NULL,
    CONSTRAINT inimigo_pk PRIMARY KEY (idInimigo),
    FOREIGN KEY (idPersonagem) REFERENCES Personagem(idPersonagem)
);
```

**Colunas:**

- `idInimigo`: Identificador único do inimigo (chave primária).
- `tipo`: Tipo do inimigo.
- `habilidade`: Habilidade do inimigo

### Moeda

A tabela **Moeda** armazena informações sobre as moedas coletáveis.

```sql
CREATE TABLE Moeda (
    idMoeda SERIAL NOT NULL,
    valor INTEGER NOT NULL,
    CONSTRAINT moeda_pk PRIMARY KEY (idMoeda)
);
```

**Colunas:**

- `idMoeda`: Identificador único da moeda (chave primária).
- `valor`: Valor da moeda.

### Loja

A tabela **Loja** armazena informações sobre as lojas presentes no jogo.

```sql
CREATE TABLE Loja (
    idLoja SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    CONSTRAINT loja_pk PRIMARY KEY (idLoja)
);
```

**Colunas:**

- `idLoja`: Identificador único da loja (chave primária).
- `nome`: Nome da loja.

### Item

A tabela **Item** armazena informações sobre os itens disponíveis no jogo.

```sql
CREATE TABLE Item (
    idItem SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    efeito VARCHAR(50),
    duração INTEGER,
    raridade VARCHAR(20),
    CONSTRAINT item_pk PRIMARY KEY (idItem)
);
```

**Colunas:**

- `idItem`: Identificador único do item (chave primária).
- `tipo`: Tipo do item.
- `efeito`: Efeito do item.
- `duração`: Duração do efeito do item.
- `raridade`: Raridade do item.

### Personagem

A tabela **Personagem** armazena informações sobre os personagens no jogo.

```sql
CREATE TABLE Personagem (
    idPersonagem SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    vida INTEGER NOT NULL,
    dano INTEGER NOT NULL,
    pontos INTEGER NOT NULL,
    idFase INTEGER, -- Removendo o NOT NULL
    tipoJogador VARCHAR(15), -- "Jogador", "Inimigo", "NPC"
    CONSTRAINT personagem_pk PRIMARY KEY (idPersonagem),
    FOREIGN KEY (idFase) REFERENCES Fase(idFase)
);
```

**Colunas:**

- `idPersonagem`: Identificador único do personagem (chave primária).
- `nome`: Nome do personagem.
- `vida`: Vida do personagem.
- `dano`: Dano causado pelo personagem.
- `pontos`: Pontos associados ao personagem.
- `idFase`: Referência a fase onde o personagem se encontra.
- `tipoJogador`: Tipo do Jogador

### Local

A tabela **Local** armazena informações sobre os locais no jogo.

```sql
CREATE TABLE Loja (
    idLoja SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    CONSTRAINT loja_pk PRIMARY KEY (idLoja)
);
```

**Colunas:**

- `idLocal`: Identificador único do local (chave primária).
- `nome`: Nome do local.

### Checkpoint

A tabela **Checkpoint** registra informações sobre os pontos de controle no jogo.

```sql

CREATE TABLE Checkpoint (
    idCheckpoint SERIAL NOT NULL,
    pontuação INTEGER NOT NULL,
    CONSTRAINT checkpoint_pk PRIMARY KEY (idCheckpoint)
);
```

**Colunas:**

- `idCheckpoint`: Identificador único do checkpoint (chave primária).
- `pontuação`: Pontuação registrada no checkpoint.

### Jogador

A tabela **Jogador** armazena informações sobre os jogadores do jogo.

```sql
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
```

**Colunas:**

- `idJogador`: Identificador único do jogador (chave primária).
- `moeda`: Quantidade de moedas do jogador.
- `idInventario`: Referência ao inventário.
- `idYoshi`: Referência ao Yoshi associado.

### Instancia

A tabela **Instancia** armazena informações sobre as instâncias de jogo.

```sql
CREATE TABLE Instancia (
    idInstancia SERIAL NOT NULL,
    vidaAtual INTEGER NOT NULL,
    moedaAtual INTEGER NOT NULL,
    idJogador INTEGER NOT NULL,
    CONSTRAINT instancia_pk PRIMARY KEY (idInstancia)
);
```

**Colunas:**

- `idInstancia`: Identificador único da instância (chave primária).
- `vidaAtual`: Vida atual da instância.
- `moedaAtual`: Quantidade de moedas na instância.
- `idJogador`: Referência ao jogador associado.

<font size="3"><p style="text-align: center">Fonte: [Gustavo Alves](https://github.com/gustaallves) e [Renan Araújo](https://github.com/renantfm4)</p></font>
