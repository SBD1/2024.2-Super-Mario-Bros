## Introdução
Linguagem de Manipulação de Dados, ou DML é a linguagem usada para manipular os dados armazenados no banco de dados relacionais, segundo Elmasri e Navathe¹ as manipulações sao de recuperação, inserção, exclusão e modificação de dados que em SQL representa os respectivos comandos: SELECT, INSERT, DELETE e UPDATE. Essa linguagem é fundamental para interagir com os dados de forma fácil e em uma linguagem de alto nível. 

## Dados
Os comandos SQL dos grupos de manipulação de dados foram separados para agrupar e tornar melhor a visualização de cada uma das manipulações de dados sob todas as tabelas do projeto.  Portanto, logo abaixo você encontrará as operaçõe: INSERT, DELETE e UPDATE.

??? "INSERT"
    #### INSERT

    ```sql

    --- Insere yoshis na tabela Yoshi ---
    INSERT INTO Yoshi (nome, idBloco) VALUES 
        ('Yoshi Verde', 5),
        ('Yoshi Azul', 9),
        ('Yoshi Vermelho', 1);


    --- Insere blocos na tabela Bloco ---
    INSERT INTO Bloco (tipo, idLocal) VALUES 
        ('Bloco de Yoshi', 1),
        ('Bloco de Moedas', 2),
        ('Bloco de Vida Extra', 1);
        ('Bloco de Cogumelo', 3);
        ('Bloco de Yoshi', 2);
        ('Bloco de Moedas', 5);
        ('Bloco de Moedas', 6);
        ('Bloco de Flor de Fogo', 4);
        ('Bloco de Yoshi', 7);
        ('Bloco de Estrela', 4);

    --- Insere canos na tabela Cano ---
    INSERT INTO Cano (idDestino) VALUES 
        ('Mundo 1-1'),
        ('Mundo 2-2'),


    --- Insere mundos na tabela Mundo ---
    INSERT INTO Mundo (nome, descrição, nivel) VALUES 
        (1, 'Um mundo inicial cheio de novas aventuras.', 1),
        (2, 'Um mundo aquático cheio dificuldades.', 2),
        (3, 'Um mundo de lava com perigos por todos os lados.', 3);

    
    --- Insere fases na tabela Fase ---
    INSERT INTO Fase (nome, nivel, idMundo) VALUES 
        ('Fase 1', 1, 1),
        ('Fase 2', 2, 2),
        ('Fase 3', 3, 3);


    --- Insere inimigos na tabela Inimigo ---
    INSERT INTO Inimigo (tipo) VALUES 
        ('Goomba'),         -- Tipo de inimigo 1
        ('Koopa Troopa'),   -- Tipo de inimigo 2
        ('Boo'),            -- Tipo de inimigo 3
        ('Thwomp'),         -- Tipo de inimigo 4
        ('Dry Bones'),      -- Tipo de inimigo 5
        ('Chain Chomp'),    -- Tipo de inimigo 6
        ('Boohemoth');      -- Tipo de inimigo 7


    --- Insere moedas na tabela Moeda ---
    INSERT INTO Moeda (valor, idBloco) VALUES 
        (1, 2),
        (5, 6),
        (10, 7);


    --- Insere lojas nas tabela Loja ---    
    INSERT INTO Loja (nome, idLocal) VALUES 
        ('Loja do Toad', 3),
        ('Loja do Yoshi', 5),
        ('Loja de Itens Raros', 7);


    --- Insere itens na tabela Item com o bloco no qual se encontra --- 
    INSERT INTO Item (tipo, efeito, duração, raridade, idBloco) VALUES 
        ('Cogumelo', 'Aumenta tamanho', 60, 'Comum', 4),
        ('Flor de Fogo', 'Atira bolas de fogo', 30, 'Raro', 8),
        ('Estrela', 'Invencibilidade', 10, 'Muito Raro', 10);


    --- Insere personagens na tabela Personagem ---
    INSERT INTO Personagem (nome, vida, dano, pontos, idLocal) VALUES 
        ('Toadette', 100, 10, 0, 6),    -- NPC 1
        ('Shy Guy', 100, 8, 0, 2),      -- NPC 2
        ('Donkey Kong', 100, 5, 0, 3);  -- NPC 2


    --- Insere locais na tabela Local para cada fase ---
    INSERT INTO Local (nome, descricao, idFase) VALUES 
        ('Castelo do Bowser', 'Um castelo cheio de lava e armadilhas.', 3), 
        ('Campos do Reino', 'Um campo verde com muitos Goombas.', 1),
        ('Caverna Aquática', 'Um local submerso com peixes hostis.', 2), 
        ('Deserto das Dunas', 'Um vasto deserto cheio de armadilhas.', 3), 
        ('Floresta Perdida', 'Uma floresta cheia de segredos ocultos.', 2),
        ('Montanhas Congeladas', 'Um local coberto de neve e gelo.', 1),
        ('Praia Ensolarada', 'Um local relaxante com perigos inesperados.', 3);


    --- Insere checkpoints na tabela Checkpoint em um local da fase ---
    INSERT INTO Checkpoint (pontuação, idLocal) VALUES 
        (100, 6),
        (200, 3),
        (300, 7);


    --- Insere jogadores na tabela Jogadores ---
    INSERT INTO Jogador (tipo, moeda, idItem, idYoshi) VALUES 
        ('Mario', 100, 1, 1), -- Jogador 1    
        ('Luigi', 50, 2, 2),  -- Jogador 2
        ('Peach', 75, 3, 3);  -- Jogador 3    

    --- Insere invatarios na tabela Inventário para cada jogador --- 
    INSERT INTO Inventário (quantidade, idJogador, IdItem) VALUES 
        (5, 1, 1),
        (3, 2, 2),
        (7, 3, 3);


    --- Insere instancia na tabela Instancia para cada jogador --- 
    INSERT INTO Instancia (vidaAtual, moedaAtual, idJogador) VALUES 
        (40, 63, 1),
        (70, 19, 2),
        (90, 25, 3);
    ```

<font size="3"><p style="text-align: center">Fonte: [Vinícius Mendes](https://github.com/yabamiah).</p></font>

??? "DELETE"
    #### DELETE

    ```sql
    BEGIN TRANSACTION;

    --- Excluir um personagem da tabela Personagem ---
    -- Primeiro deletamos os registros dependentes da tabela Local (referenciada por Checkpoint, Loja, etc.)
    DELETE FROM Checkpoint WHERE idLocal = 1; -- Supondo que o personagem está no Local 1
    DELETE FROM Loja WHERE idLocal = 1;
    DELETE FROM Personagem WHERE idPersonagem = 1;


    --- Excluir um bloco da tabela Bloco ---
    -- Primeiro deletamos os registros dependentes (Item e Moeda)
    DELETE FROM Item WHERE idBloco = 1; -- Supondo que o bloco com id 1 está associado
    DELETE FROM Moeda WHERE idBloco = 1;
    -- Depois, deletamos o bloco
    DELETE FROM Bloco WHERE idBloco = 1;


    --- Excluir um jogador da tabela Jogador ---
    -- Primeiro deletamos os registros dependentes (Instancia e Inventário)
    DELETE FROM Instancia WHERE idJogador = 1;
    DELETE FROM Inventário WHERE idJogador = 1;
    -- Depois, deletamos o jogador
    DELETE FROM Jogador WHERE idJogador = 1;


    --- Excluir um Yoshi da tabela Yoshi ---
    -- Primeiro deletamos os registros dependentes (Jogador)
    DELETE FROM Jogador WHERE idYoshi = 1; -- Supondo que o Yoshi com id 1 está associado
    -- Deletamos o Yoshi
    DELETE FROM Yoshi WHERE idYoshi = 1;


    --- Excluir uma fase da tabela Fase ---
    -- Primeiro deletamos os registros dependentes (Local)
    DELETE FROM Local WHERE idFase = 1; -- Supondo que a fase com id 1 está associada
    -- Deletamos a fase
    DELETE FROM Fase WHERE idFase = 1;


    --- Excluir um mundo da tabela Mundo ---
    -- Primeiro deletamos os registros dependentes (Fase)
    DELETE FROM Fase WHERE idMundo = 1; -- Supondo que o mundo com id 1 está associado
    -- Deletamos o mundo
    DELETE FROM Mundo WHERE idMundo = 1;


    --- Excluir um cano da taela Cano ---
    -- Primeiro deletamos os registros dependentes (Mundo)
    DELETE FROM Mundo WHERE idDestino = 1; -- Supondo que o cano com id 1 está associado
    -- Deletamos o cano
    DELETE FROM Cano WHERE idCano = 1;


    --- Excluir um item da tabela Item ---
    -- Deletamos o item diretamente, pois depende apenas de Bloco
    DELETE FROM Item WHERE idItem = 1;


    --- Excluir um moeda da tabela Moeda ---
    -- Deletamos a moeda diretamente, pois depende apenas de Bloco
    DELETE FROM Moeda WHERE idMoeda = 1;


    --- Excluir um inimigo da tabela Inimigo ---
    -- Deletamos o inimigo diretamente, pois não depende de nenhuma outra tabela
    DELETE FROM Inimigo WHERE idInimigo = 1;


    --- Excluir um loja da tabela Loja ---
    -- Deletamos a loja diretamente, considerando sua dependência de Local
    DELETE FROM Loja WHERE idLoja = 1;


    --- Excluir um checkpoint da tabela Checkpoint ---
    -- Deletamos o checkpoint diretamente, considerando sua dependência de Local
    DELETE FROM Checkpoint WHERE idCheckpoint = 1;
    ```

<font size="3"><p style="text-align: center">Fonte: [Vinícius Mendes](https://github.com/yabamiah).</p></font>


??? "UPDATE"
    #### UPDATE

    ```sql

    --- Atualizar um personagem da tabela Personagem ---
    -- Atualizar o nome e a vida de um personagem com `idPersonagem = 1`
    UPDATE Personagem 
    SET nome = 'Wario', vida = 100 
    WHERE idPersonagem = 1;

    --- Atualizar um bloco da tabela Bloco ---
    -- Atualizar o tipo de bloco com `idBloco = 1`
    UPDATE Bloco 
    SET tipo = 'Bloco Surpresa' 
    WHERE idBloco = 1;

    --- Atualizar um jogador da tabela Jogador ---
    -- Atualizar o tipo e a moeda de um jogador com `idJogador = 1`
    UPDATE Jogador 
    SET tipo = 'Toad', moeda = 50 
    WHERE idJogador = 1;

    --- Atualizar um Yoshi da tabela Yoshi ---
    -- Atualizar o nome de um Yoshi com `idYoshi = 1`
    UPDATE Yoshi 
    SET nome = 'Yoshi Rosa' 
    WHERE idYoshi = 1;

    --- Atualizar uma fase da tabela Fase ---
    -- Atualizar o nível e o nome de uma fase com `idFase = 1`
    UPDATE Fase 
    SET nivel = 2, nome = 'Fase da Floresta' 
    WHERE idFase = 1;

    --- Atualizar um mundo da tabela Mundo ---
    -- Atualizar o nome e a descrição de um mundo com `idMundo = 1`
    UPDATE Mundo 
    SET nome = 3, descricao = 'Um mundo cheio de estrelas.' 
    WHERE idMundo = 1;

    --- Atualizar um cano da tabela Cano ---
    -- Atualizar o destino de um cano com `idCano = 1`
    UPDATE Cano 
    SET idDestino = 'Mundo 1-3' 
    WHERE idCano = 1;

    --- Atualizar um item da tabela Item ---
    -- Atualizar o tipo e a raridade de um item com `idItem = 1`
    UPDATE Item 
    SET tipo = 'Cogumelo Verde', 'Recupera vida', raridade = 'Comum' 
    WHERE idItem = 1;

    --- Atualizar uma moeda da tabela Moeda ---
    -- Atualizar o valor de uma moeda com `idMoeda = 1`
    UPDATE Moeda 
    SET valor = 5 
    WHERE idMoeda = 1;

    --- Atualizar um inimigo da tabela Inimigo ---
    -- Atualizar o tipo de um inimigo com `idInimigo = 1`
    UPDATE Inimigo 
    SET tipo = 'Peixe' 
    WHERE idInimigo = 1;

    --- Atualizar uma loja da tabela Loja ---
    -- Atualizar o nome de uma loja com `idLoja = 1`
    UPDATE Loja 
    SET nome = 'Loja do Tião' 
    WHERE idLoja = 1;

    --- Atualizar um checkpoint da tabela Checkpoint ---
    -- Atualizar a pontuação de um checkpoint com `idCheckpoint = 1`
    UPDATE Checkpoint 
    SET pontuação = 150 
    WHERE idCheckpoint = 1;

    --- Atualizar uma instância da tabela Instancia ---
    -- Atualizar a vida e a moeda atual de uma instância com `idInstancia = 1`
    UPDATE Instancia 
    SET vidaAtual = 80, moedaAtual = 20 
    WHERE idInstancia = 1;

    --- Atualizar um inventário da tabela Inventário ---
    -- Atualizar a quantidade de um item no inventário com `idInventário = 1`
    UPDATE Inventário 
    SET quantidade = 10 
    WHERE idInventário = 1;

    --- Atualizar um local da tabela Local ---
    -- Atualizar o nome e a descrição de um local com `idLocal = 1`
    UPDATE Local 
    SET nome = 'Castelo do Wendy', descricao = 'Um castelo perigoso cheio de armadilhas.' 
    WHERE idLocal = 1;
    ```

<font size="3"><p style="text-align: center">Fonte: [Vinícius Mendes](https://github.com/yabamiah).</p></font>



## <a>Referência Bibliográfica</a>

> <a id="REF1" href="#anchor_1">1.</a> ELMASRI, Ramez; NAVATHE, Shamkant B. Sistemas de banco de dados. Tradução: Daniel Vieira. Revisão técnica: Enzo Seraphim; Thatyana de Faria Piola Seraphim. 6. ed. São Paulo: Pearson Addison Wesley, 2011. Capítulo 2 Conceitos e arquitetura do sistema de banco de dados, tópico 2.3 Linguagens e interfaces do banco de dados, páginas 24 e 25.