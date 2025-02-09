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
| `moeda`      | Quantidade de moedas do jogador             | `INTEGER`    | -       | Not Null                                           |
| `idYoshi`    | Referência ao Yoshi associado               | `INTEGER`    | -       | FK                                                 |
| `idInventario` | Referência ao inventário do jogador       | `INTEGER`    | -       | FK                                                 |

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
| `habilidade`       | Habilidade do inimigo                   | `VARCHAR`    | 15      | Not Null               |

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
| `idItem`   | Referência ao item contido no bloco      | `INTEGER`    | -       | FK                     |
| `idYoshi`  | Referência ao Yoshi contido no bloco     | `INTEGER`    | -       | FK                     |
| `idMoeda`  | Referência à moeda contida no bloco      | `INTEGER`    | -       | FK                     |

---

## **Tabela: `local`**
Armazena informações dos locais.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `idLocal`      | Identificador único do local             | `SERIAL`     | -       | PK, Not Null           |
| `nome`         | Nome do local                            | `VARCHAR`    | 50      | Not Null               |
| `regiao`       | Região do local                          | `VARCHAR`    | 50      | Not Null               |
| `descricao`    | Descrição do local                       | `TEXT`       | -       | -                      |
| `idFase`       | Referência à fase relacionada ao local   | `INTEGER`    | -       | FK, Not Null           |
| `idBloco`      | Referência ao bloco associado ao local   | `INTEGER`    | -       | FK                     |
| `idPersonagem` | Referência ao personagem associado ao local | `INTEGER`    | -       | FK                     |
| `idLoja`       | Referência à loja associada ao local     | `INTEGER`    | -       | FK                     |
| `idCheckpoint` | Referência ao checkpoint associado ao local | `INTEGER`    | -       | FK                     |

---

## **Tabela: `personagem`**
Armazena informações sobre os personagens no jogo.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `idPersonagem` | Identificador único do personagem        | `SERIAL`     | -       | PK, Not Null           |
| `nome`         | Nome do personagem                       | `VARCHAR`    | 20      | Not Null               |
| `vida`         | Vida do personagem                       | `INTEGER`    | -       | Not Null               |
| `dano`         | Dano causado pelo personagem             | `INTEGER`    | -       | Not Null               |
| `pontos`       | Pontos associados ao personagem          | `INTEGER`    | -       | Not Null               |
| `idLocal`      | Referência ao local onde o personagem se encontra | `INTEGER`    | -       | FK                     |
| `tipoJogador`  | Tipo de jogador (Jogador, Inimigo, NPC)  | `VARCHAR`    | 15      | Not Null               |

---

## **Tabela: `inventario`**
Armazena informações sobre os itens no inventário.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `idInventario` | Identificador único do inventário        | `SERIAL`     | -       | PK, Not Null           |
| `quantidade`   | Quantidade de itens                      | `INTEGER`    | -       | Not Null               |
| `idItem`       | Referência ao item                       | `INTEGER`    | -       | FK, Not Null           |
| `idPersonagem` | Referência ao personagem associado ao inventário | `INTEGER`    | -       | FK, Not Null           |

---

## **Tabela: `instancia`**
Armazena informações sobre as instâncias de jogo.

| Nome           | Descrição                                 | Tipo de dado | Tamanho | Restrições de domínio |
|----------------|-------------------------------------------|--------------|---------|------------------------|
| `idInstancia`  | Identificador único da instância         | `SERIAL`     | -       | PK, Not Null           |
| `vidaAtual`    | Vida atual da instância                  | `INTEGER`    | -       | Not Null               |
| `moedaAtual`   | Quantidade de moedas na instância        | `INTEGER`    | -       | Not Null               |
| `idJogador`    | Referência ao jogador associado à instância | `INTEGER`    | -       | FK, Not Null           |