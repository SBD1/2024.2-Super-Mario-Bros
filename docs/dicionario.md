# **Dicionário de Dados - Jogo Mario**

## **Tabela: `tipoPersonagem`**
Armazena valores de constantes relevantes ao jogo, como `pontuaçãoBase` e `vidaBase`.

| Nome  | Descrição                                   | Tipo de dado | Tamanho | Restrições de domínio |
|-------|---------------------------------------------|--------------|---------|------------------------|
| `nome`  | Nome que identifica unicamente uma constante | `VARCHAR`    | 20      | PK, Not Null           |
| `valor` | Valor numérico da constante               | `INTEGER`    | -       | Not Null               |

---

## **Tabela: `jogador`**
Armazena as informações referentes ao personagem jogável do usuário.

| Nome         | Descrição                                    | Tipo de dado | Tamanho | Restrições de domínio                               |
|--------------|----------------------------------------------|--------------|---------|---------------------------------------------------|
| `nome`       | Nome único do personagem                    | `VARCHAR`    | 15      | PK, FK, Not Null                                  |
| `vidaMax`    | O limite de vida do personagem              | `INTEGER`    | -       | Not Null, Default = 50                            |
| `vidaAtual`  | A vida atual do personagem                  | `INTEGER`    | -       | Not Null, Default = 50, Check (`vidaAtual <= vidaMax`) |
| `faseAtual`  | Determina a fase atual do personagem        | `INTEGER`    | -       | FK, Not Null, Default = 1                         |
| `itemMagico` | Referência ao item mágico                   | `INTEGER`    | -       | FK                                                 |
| `areaAtual`  | Referência à área onde o jogador está       | `VARCHAR`    | 35      | FK, Not Null                                       |

---

## **Tabela: `inimigo`**
Armazena as informações referentes aos inimigos.

| Nome               | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio |
|--------------------|------------------------------------------|--------------|---------|------------------------|
| `nome`             | Nome único do inimigo                   | `VARCHAR`    | 15      | PK, FK, Not Null       |
| `vidaMax`          | O limite de vida do inimigo             | `INTEGER`    | -       | Not Null               |
| `pontos`           | Pontuação ao derrotar o inimigo         | `INTEGER`    | -       | Not Null               |
| `dano`             | Dano causado pelo inimigo               | `INTEGER`    | -       | Not Null               |
| `velocidade`       | Velocidade do inimigo                   | `INTEGER`    | -       | Not Null               |
| `pontosExperiencia`| Experiência ganha ao derrotar o inimigo | `INTEGER`    | -       | Not Null               |
| `nivel`            | Referência ao nível do inimigo          | `INTEGER`    | -       | FK, Not Null           |

---

## **Tabela: `inimigoConcreto`**
Armazena as instâncias dos inimigos gerados no jogo.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `nomeConcreto` | Nome único de uma instância de inimigo    | `VARCHAR`    | 15      | PK, Not Null           |
| `vidaAtual`    | A vida atual da instância                 | `INTEGER`    | -       | Not Null               |
| `inimigo`      | Referência ao inimigo base                | `VARCHAR`    | 15      | FK, Not Null           |
| `areaAtual`    | Área onde o inimigo se encontra           | `VARCHAR`    | 35      | FK, Not Null           |
| `loot`         | Referência ao item ganho ao derrotar      | `INTEGER`    | -       | FK, Not Null           |

---

## **Tabela: `mundo`**
Armazena os mundos do jogo.

| Nome              | Descrição                                | Tipo de dado | Tamanho | Restrições de domínio |
|-------------------|------------------------------------------|--------------|---------|------------------------|
| `idMundo`         | Identificador único do mundo            | `SERIAL`     | -       | PK, Not Null           |
| `nome`            | Nome do mundo                           | `VARCHAR`    | 50      | Not Null               |
| `descricao`       | Descrição detalhada do mundo            | `TEXT`       | -       | -                      |
| `nivel_inicial_id`| Referência ao nível inicial do mundo     | `INTEGER`    | -       | FK, Not Null           |

---

## **Tabela: `fase`**
Armazena as fases do jogo.

| Nome              | Descrição                                    | Tipo de dado | Tamanho | Restrições de domínio |
|-------------------|----------------------------------------------|--------------|---------|------------------------|
| `idNivel`         | Referência ao nível atual da fase           | `INTEGER`    | -       | PK, FK, Not Null       |
| `quantidadeFases` | Número de fases necessárias para o próximo mundo | `INTEGER`    | -       | Not Null               |

---

## **Tabela: `bloco`**
Armazena informações dos blocos.

| Nome       | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|------------|-------------------------------------------|--------------|---------|------------------------|
| `idBloco`  | Identificador único do bloco             | `SERIAL`     | -       | PK, Not Null           |
| `tipo`     | Tipo do bloco                            | `VARCHAR`    | 30      | Not Null               |
| `conteudo` | Conteúdo do bloco (ex.: moeda, item)     | `VARCHAR`    | 50      | -                      |
| `nivel_id` | Referência ao nível onde o bloco aparece | `INTEGER`    | -       | FK, Not Null           |
| `posicao`  | Posição do bloco no nível                | `VARCHAR`    | 10      | Not Null               |

---

## **Tabela: `checkpoint`**
Armazena informações dos checkpoints.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `idCheckpoint` | Identificador único do checkpoint        | `SERIAL`     | -       | PK, Not Null           |
| `nivel_id`     | Referência ao nível em que o checkpoint está | `INTEGER`    | -       | FK, Not Null           |
| `posicao`      | Posição do checkpoint                    | `VARCHAR`    | 10      | Not Null               |

---

## **Tabela: `cano`**
Armazena informações sobre os canos.

| Nome       | Descrição                                   | Tipo de dado | Tamanho | Restrições de domínio |
|------------|---------------------------------------------|--------------|---------|------------------------|
| `idCano`   | Identificador único do cano                | `SERIAL`     | -       | PK, Not Null           |
| `origem`   | Área de origem                             | `VARCHAR`    | 35      | FK, Not Null           |
| `destino`  | Área de destino                            | `VARCHAR`    | 35      | FK, Not Null           |
| `requisito`| Requisitos para usar o cano                | `TEXT`       | -       | -                      |