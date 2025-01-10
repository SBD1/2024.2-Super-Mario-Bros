## Introdução

O DDL (Data Definition Language) é uma parte essencial do SQL (Structured Query Language), responsável pela definição da estrutura de um banco de dados.  

Com a DDL, é possível criar, alterar e excluir objetos no banco de dados, como tabelas, índices, esquemas, visões e outros elementos relacionados à organização dos dados.  

Por meio dela, desenvolvedores e administradores podem configurar a estrutura base que será utilizada para armazenar e gerenciar informações, garantindo uma organização eficiente e flexível para os sistemas que utilizam bancos de dados relacionais.


## Descrição das Tabelas e Entidades

### Yoshi

A tabela **Yoshi** armazena informações sobre a entidade Yoshi no sistema.

```sql
CREATE TABLE IF NOT EXISTS Yoshi (
    idYoshi SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    idBloco INTEGER NOT NULL,

    CONSTRAINT yoshi_pk PRIMARY KEY (idYoshi)
);
```

**Colunas:**

- `idYoshi`: Identificador único de Yoshi (chave primária).
- `nome`: Nome de Yoshi.
- `idBloco`: Referência ao bloco associado.

### Bloco

A tabela **Bloco** armazena detalhes sobre os blocos existentes no jogo.

```sql
CREATE TABLE IF NOT EXISTS Bloco (
    idBloco SERIAL NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    idLocal INTEGER NOT NULL,

    CONSTRAINT bloco_pk PRIMARY KEY (idBloco)
);
```

**Colunas:**

- `idBloco`: Identificador único do bloco (chave primária).
- `tipo`: Tipo do bloco.
- `idLocal`: Referência ao local relacionado ao bloco.

### Cano

A tabela **Cano** representa conexões entre diferentes áreas.

```sql
CREATE TABLE IF NOT EXISTS Cano (
    idCano SERIAL NOT NULL,
    idDestino VARCHAR(35) NOT NULL,

    CONSTRAINT cano_pk PRIMARY KEY (idCano)
);
```

**Colunas:**

- `idCano`: Identificador único do cano (chave primária).
- `idDestino`: Referência ao destino conectado pelo cano.

### Mundo

A tabela **Mundo** armazena informações sobre os mundos disponíveis no jogo.

```sql
CREATE TABLE IF NOT EXISTS Mundo (
    idMundo SERIAL NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descrição TEXT,
    nivel INTEGER NOT NULL,

    CONSTRAINT mundo_pk PRIMARY KEY (idMundo),
    FOREIGN KEY (nome) REFERENCES Cano(idCano)
);
```

**Colunas:**

- `idMundo`: Identificador único do mundo (chave primária).
- `nome`: Nome do mundo.
- `descrição`: Detalhes descritivos sobre o mundo.
- `nivel`: Nível associado ao mundo.

### Fase

A tabela **Fase** organiza os estágios do jogo.

```sql
CREATE TABLE IF NOT EXISTS Fase (
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
CREATE TABLE IF NOT EXISTS Inventário (
    idIventário SERIAL NOT NULL,
    quantidade INTEGER NOT NULL,
    idJogador INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,

    CONSTRAINT inventário_pk PRIMARY KEY (idIventário)
);
```

**Colunas:**

- `idIventário`: Identificador único do inventário (chave primária).
- `quantidade`: Quantidade de itens.
- `idJogador`: Referência ao jogador.
- `IdItem`: Referência ao item.

### Inimigo

A tabela **Inimigo** registra detalhes sobre os inimigos no jogo.

```sql
CREATE TABLE IF NOT EXISTS Inimigo (
    idInimigo SERIAL NOT NULL,
    tipo VARCHAR(15) NOT NULL,

    CONSTRAINT inimigo_pk PRIMARY KEY (idInimigo)
);
```

**Colunas:**

- `idInimigo`: Identificador único do inimigo (chave primária).
- `tipo`: Tipo do inimigo.

### Moeda

A tabela **Moeda** armazena informações sobre as moedas coletáveis.

```sql
CREATE TABLE IF NOT EXISTS Moeda (
    idMoeda SERIAL NOT NULL,
    valor INTEGER NOT NULL,
    idBloco INTEGER NOT NULL,

    CONSTRAINT moeda_pk PRIMARY KEY (idMoeda),
    FOREIGN KEY (idBloco) REFERENCES Bloco(idBloco)
);
```

**Colunas:**

- `idMoeda`: Identificador único da moeda (chave primária).
- `valor`: Valor da moeda.
- `idBloco`: Referência ao bloco onde a moeda está armazenada.
