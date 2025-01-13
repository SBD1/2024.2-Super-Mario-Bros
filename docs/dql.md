## Introdução

A Data Query Language (DQL) é um subconjunto da linguagem SQL utilizado para consultar e recuperar dados armazenados em um banco de dados. O principal objetivo da DQL é permitir que os usuários extraiam informações relevantes e significativas de uma base de dados, conforme suas necessidades. O foco da DQL não é alterar ou manipular a estrutura ou os dados, mas sim realizar consultas.

## Consultas

### Listar todos os Yoshis e seus blocos associados

```sql
SELECT Yoshi.nome, Bloco.tipo
FROM Yoshi
JOIN Bloco ON Yoshi.idBloco = Bloco.idBloco;
```

### Listar todos os inimigos e seu tipo

```sql
SELECT idInimigo, tipo
FROM Inimigo;
```

### Listar todos os itens no inventário de um jogador específico

```sql
SELECT Item.tipo, Inventário.quantidade
FROM Inventário
JOIN Item ON Inventário.IdItem = Item.idItem
WHERE Inventário.idJogador = 1;
```

### Listar o jogador seu Yoshi e suas moedas

```sql
SELECT Jogador.idJogador, Jogador.moeda, Yoshi.nome
FROM Jogador
JOIN Yoshi ON Jogador.idYoshi = Yoshi.idYoshi;
```

### Listar todos os checkpoints de um determinado local

```sql
SELECT Checkpoint.idCheckpoint, Checkpoint.pontuação
FROM Checkpoint
JOIN Local ON Checkpoint.idLocal = Local.idLocal
WHERE Local.nome = 'Mundo 1';
```

### Listar todos os itens de um bloco específico

```sql
SELECT Item.tipo, Item.efeito
FROM Item
JOIN Bloco ON Item.idBloco = Bloco.idBloco
WHERE Bloco.idBloco=2;
```

### Listar todas as fases e seus mundos

```sql
SELECT Fase.nome, Mundo.nome
FROM Fase
JOIN Mundo ON Fase.idMundo = Mundo.idMundo;
```
