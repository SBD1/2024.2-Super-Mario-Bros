# Álgebra Relacional

## Introdução

A álgebra relacional é um conjunto de operações matemáticas utilizadas para manipular e consultar dados armazenados em bancos de dados relacionais. Ela serve como a base teórica para a linguagem SQL (Structured Query Language), que é amplamente utilizada para gerenciar e consultar bancos de dados.

\[
\pi_{\text{nome\_item}, \text{quantidade}}((\sigma_{\text{nome} = 'Mario'}(\text{Jogador}) \bowtie_{\text{id\_jogador} = \text{id\_jogador}} \text{Inventario}) \bowtie_{\text{id\_item} = \text{id\_item}} \sigma_{\text{nome\_item} = 'Cogumelo'}(\text{Item}))
\]

Álgebra Relacional para a busca de um cogumelo no inventário do jogador.  
**Autores:** Alana, Fabio, Gustavo, Renan e Vinícius.

---

## Fundamentos da Álgebra Relacional

Na álgebra relacional, os dados são organizados em relações (ou tabelas), que são compostas por tuplas (linhas) e atributos (colunas). Cada relação é uma representação de uma entidade ou um relacionamento entre entidades no mundo real. As operações da álgebra relacional permitem a manipulação dessas relações para produzir novas relações, facilitando a consulta e a análise dos dados.

---