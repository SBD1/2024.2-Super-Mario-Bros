
# Dicionário de Dados - Jogo Mario

## Tabela: `tipoPersonagem`
### Descrição
Armazenará valores de constantes relevantes ao jogo, como pontuaçãoBase e vidaBase.

### Observações
Esta tabela não possui nenhum relacionamento.

| Nome  | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------|-----------|--------------|---------|-----------------------|
| nome  | Nome que irá identificar unicamente uma constante | VARCHAR | 20 | PK, Not Null |
| valor | Valor numérico da constante | INTEGER | - | Not Null |

---

## Tabela: `jogador`
### Descrição
Armazenará as informações referentes ao personagem jogável do usuário.

### Observações
Essa tabela é uma especificação de Personagem. A tabela `tipoPersonagem` será a responsável por armazenar as chaves e o tipo da especificação.

| Nome          | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------------|-----------|--------------|---------|-----------------------|
| nome          | Nome que irá identificar unicamente o personagem do jogador | VARCHAR | 15 | PK, FK, Not Null |
| vidaMax       | O limite de vida do personagem | INTEGER | - | Not Null, Default = 50 |
| vidaAtual     | A vida atual do personagem | INTEGER | - | Not Null, Default = 50, Check(vidaAtual <= vidaMax) |
| faseAtual     | Determina a fase atual do personagem | INTEGER | - | Not Null, Default = 0 |
| itemMagico    | Referência ao item mágico que o personagem pode usar | INTEGER | - | FK |
| areaAtual     | Referência à área que o personagem se encontra dentro do mapa do jogo | VARCHAR | 35 | FK, Not Null |
| fase          | Referência à fase atual do personagem | INTEGER | - | FK, Not Null, Default = 1 |

---

## Tabela: `inimigo`
### Descrição
Armazenará as informações referentes a um inimigo do jogo. Um inimigo é uma criatura com o objetivo de matar o personagem do jogador.

### Observações
Essa tabela é uma especificação de Personagem. A tabela `tipoPersonagem` será responsável por armazenar as chaves e o tipo da especificação. Esta tabela define uma "ficha" de inimigo que irá gerar "Inimigos Concretos".

| Nome              | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------------------|-----------|--------------|---------|-----------------------|
| nome              | Nome que irá identificar unicamente o personagem do inimigo | VARCHAR | 15 | PK, FK, Not Null |
| vidaMax           | O limite de vida do inimigo | INTEGER | - | Not Null |
| pontos            | O número de pontos define a força do inimigo | INTEGER | - | Not Null |
| dano              | O número de dano define a força do inimigo | INTEGER | - | Not Null |
| velocidade        | O número de velocidade do inimigo | INTEGER | - | Not Null |
| pontosExperiencia | O número de pontos de experiência que um jogador ganha ao derrotar o inimigo | INTEGER | - | Not Null |
| nivel             | Referência ao nível atual do inimigo | INTEGER | - | FK, Not Null |

---

## Tabela: `tipoPersonagem`
### Descrição
Armazenará a relação de nome do Personagem com o tipo dele, Jogador ou Inimigo.

### Observações
Esta tabela diferencia quais personagens são Jogadores e quais são Inimigos.

| Nome              | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------------------|-----------|--------------|---------|-----------------------|
| nome              | Nome que irá identificar unicamente um personagem | VARCHAR | 15 | PK, Not Null |
| tipo              | Especifica se o Personagem é um Jogador ou um Inimigo | CHAR | 1 | Check (tipo == 'J' or tipo == 'I') |

---

## Tabela: `fase`
### Descrição
Armazenará os dados do personagem e se ele chegou à fase necessária para mudar de mundo.

| Nome    | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------|-----------|--------------|---------|-----------------------|
| idNivel | Número sequencial que indica o nível do personagem | INTEGER | - | PK, Not Null, Identity |
| Fase    | Número de fases necessário para mudar de mundo | INTEGER | - | Not Null |

---

## Tabela: `inimigoConcreto`
### Descrição
Armazenará as informações da instância de um inimigo.

### Observações
Esta tabela existe para reutilizar informações da tabela `inimigo` e evitar redundâncias e sobrecarga no banco.

| Nome        | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------------|-----------|--------------|---------|-----------------------|
| nomeConcreto| Nome que identifica unicamente uma instância de Inimigo | VARCHAR | 15 | PK, Not Null |
| vidaAtual   | A vida atual da instância de Inimigo | INTEGER | - | Not Null |
| inimigo     | Referência ao Inimigo gerador desta instância | VARCHAR | 15 | FK, Not Null |
| areaAtual   | Referência à área onde o personagem se encontra dentro do mapa do jogo | VARCHAR | 35 | FK, Not Null |
| loot        | Referência ao item que o jogador ganha ao derrotar o inimigo | INTEGER | - | FK, Not Null |

---

## Tabela: `inventario`
### Descrição
Armazenará informações sobre o inventário do jogador, incluindo o jogador associado e a carga máxima que ele pode carregar.

| Nome        | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------------|-----------|--------------|---------|-----------------------|
| jogador     | Identificador do jogador | VARCHAR | 15 | PK, FK, Not Null |
| cargaMaxima | Carga máxima do jogador (até 28 itens) | INTEGER | - | Not Null, Check (cargaMaxima ≥ 28) |

---

## Tabela: `tipoItem`
### Descrição
Armazenará os diferentes tipos de itens que podem existir no jogo.

### Observações
A classificação indicará qual especificação o item possui, como cogumelo, flor de fogo, super estrela, etc.

| Nome         | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|--------------|-----------|--------------|---------|-----------------------|
| nome         | Nome do item | VARCHAR | 30 | PK, Identity |
| classificacao| Classificação do item | VARCHAR | 15 | Not Null, Check (classificacao in (Consumivel)) |

---

## Tabela: `itemInventario`
### Descrição
Armazenará os itens que estão no inventário de cada jogador.

| Nome    | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------|-----------|--------------|---------|-----------------------|
| jogador | Identificador do jogador que possui o item | VARCHAR | 15 | PK, FK, Not Null |
| item    | Identificador do item no inventário do jogador | VARCHAR | 30 | PK, FK, Not Null |

---

## Tabela: `magico`
### Descrição
Armazenará informações sobre itens mágicos, como nome, descrição, peso e efeitos.

| Nome          | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------------|-----------|--------------|---------|-----------------------|
| nome          | Nome do item mágico | VARCHAR | 15 | PK, FK, Not Null |
| areaAtual     | Área onde o item pode ser encontrado | VARCHAR | 30 | FK |
| descricao     | Descrição detalhada do item | TEXT | - | - |
| peso          | Peso do item | INTEGER | - | Check (peso >= 0) |
| modEfeito     | Modificador de efeito | INTEGER | - | Check (modEfeito >= 0) |
| modForca      | Modificador de poder mágico | INTEGER | - | Check (modForca >= 0) |
| modVelocidade | Modificador de velocidade | INTEGER | - | Check (modVelocidade >= 0) |
| tempoDeRecarga| Tempo de recarga em segundos | INTEGER | - | Check (tempoDeRecarga >= 0) |
| tempoAtual    | Tempo atual em segundos | INTEGER | - | Check (tempoAtual >= 0) |

---

## Tabela: `consumíveis`
### Descrição
Armazenará informações sobre itens consumíveis, como poções.

| Nome         | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|--------------|-----------|--------------|---------|-----------------------|
| nome         | Nome do item consumível | VARCHAR | 15 | PK, FK, Not Null |
| areaAtual    | Área onde o item pode ser encontrado | VARCHAR | 30 | FK |
| descricao    | Descrição detalhada do item | TEXT | - | - |
| peso         | Peso do item | INTEGER | - | Check (peso >= 0) |
| vidaRecuperada| Quantidade de vida recuperada | INTEGER | - | Check (vidaRecuperada >= 0) |
| areaCano     | Área para a qual o jogador se teletransporta |

 VARCHAR | 30 | FK |

---

## Tabela: `regiao`
### Descrição
Armazenará informações referentes às diferentes regiões existentes no mapa.

| Nome    | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------|-----------|--------------|---------|-----------------------|
| nome    | Nome que identifica unicamente uma região | VARCHAR | 35 | PK, Not Null |
| descricao | Descrição detalhada da região | TEXT | - | Not Null |
| nivel   | Nível da região utilizado para balancear combates | INTEGER | - | Not Null |

---

## Tabela: `area`
### Descrição
Armazenará informações referentes às diferentes áreas dentro de uma região.

| Nome        | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|-------------|-----------|--------------|---------|-----------------------|
| nome        | Nome que identifica unicamente uma área | VARCHAR | 15 | PK, Not Null |
| descricao   | Descrição detalhada da área | TEXT | - | - |
| regiaoAtual | Região à qual a área pertence | VARCHAR | 35 | FK, Not Null |
| norte       | Coordenada norte da área | INTEGER | - | CK1 |
| sul         | Coordenada sul da área | INTEGER | - | CK1 |
| leste       | Coordenada leste da área | INTEGER | - | CK1 |
| oeste       | Coordenada oeste da área | INTEGER | - | CK1 |
| desafio     | Desafio associado à área | INTEGER | - | FK, Not Null |

---

## Tabela: `mundo`
### Descrição
Armazenará informações sobre os mundos do jogo, que são desbloqueados após concluir a última fase.

| Nome    | Descrição | Tipo de dado | Tamanho | Restrições de domínio |
|---------|-----------|--------------|---------|-----------------------|
| id      | Número que identifica unicamente um desafio | SERIAL | - | PK |
| tipo    | Tipo de desafio (armadilha ou desafio) | CHAR | 1 | Check (tipo == 'a' or tipo == 'd') |