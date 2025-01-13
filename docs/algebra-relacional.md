## Introdução

Àlgebra relacional é a base teórica para manipular e consultar dados em bancos de dados relacionais. Ela utiliza um conjunto de operações para transformar ou combinar relações (tabelas), gerando novas relações sem alterar os dados originais. Essencial para sistemas de banco de dados, a álgebra relacional é usada internamente para processar e otimizar consultas SQL, fornecendo uma linguagem formal para descrever operações sobre dados.

## Consultas

### Listar todos os Yoshis e seus blocos associados

π(nome, tipo)(Yoshi⋈Bloco)

### Listar todos os inimigos e seu tipo

π(idInimigo, tipo)(Inimigo)

### Listar todos os itens no inventário de um jogador específico

π(tipo, quantidade)(σidJogador = 1)(Inventário⋈Item)

### Listar o jogador seu Yoshi e suas moedas

π(idJogador, moeda, nome)(Jogador⋈Yoshi)

### Listar todos os checkpoints de um determinado local

π(idCheckpoint, pontuação)(σnome = 'Mundo 1')(Checkpoint⋈Local)

### Listar todos os itens de um bloco específico

π(tipo, efeito)(σidBloco = 2)(Item⋈Bloco)

### Listar todas as fases e seus mundos

πnome (Fase), nome (Mundo)(Fase⋈Mundo)
