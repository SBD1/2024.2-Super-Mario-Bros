-- Conecta ao banco supermario
\c supermario;

--- Insere mundos na tabela Mundo ---
INSERT INTO Mundo (nome, descrição, nivel) VALUES 
('Mundo 1', 'Um mundo inicial cheio de novas aventuras.', 1),
('Mundo 2', 'Um mundo aquático cheio de dificuldades.', 2),
('Mundo 3', 'Um mundo de lava com perigos por todos os lados.', 3);

--- Insere fases na tabela Fase ---
INSERT INTO Fase (nome, nivel, idMundo) VALUES 
('Fase 1', 1, 1),
('Fase 2', 2, 2),
('Fase 3', 3, 3);

--- Insere Yoshis na tabela Yoshi ---
INSERT INTO Yoshi (nome) VALUES 
('Yoshi Verde'),
('Yoshi Azul'),
('Yoshi Vermelho');

--- Insere moedas na tabela Moeda ---
INSERT INTO Moeda (valor) VALUES 
(1),
(5),
(10);

--- Insere itens na tabela Item ---
INSERT INTO Item (tipo, efeito, duração, raridade) VALUES 
('Cogumelo', 'Aumenta tamanho', 60, 'Comum'),
('Flor de Fogo', 'Atira bolas de fogo', 30, 'Raro'),
('Estrela', 'Invencibilidade', 10, 'Muito Raro');

--- Insere blocos na tabela Bloco ---
INSERT INTO Bloco (tipo, iditem, idyoshi, idmoeda) VALUES 
('Bloco de Yoshi', NULL, 1, NULL),  -- Bloco de Yoshi - Referencia o Yoshi Verde
('Bloco de Moedas', NULL, NULL, 1),  -- Bloco de Moedas - Referencia a Moeda de valor 1
('Bloco de Vida Extra', 1, NULL, NULL),  -- Bloco de Vida Extra - Referencia o Item Cogumelo
('Bloco de Cogumelo', 1, NULL, NULL),  -- Bloco de Cogumelo - Referencia o Item Cogumelo
('Bloco de Flor de Fogo', 2, NULL, NULL),  -- Bloco de Flor de Fogo - Referencia o Item Flor de Fogo
('Bloco de Estrela', 3, NULL, NULL);  -- Bloco de Estrela - Referencia o Item Estrela


--- Insere personagens na tabela Personagem ---
INSERT INTO Personagem (nome, vida, dano, pontos, idFase, tipoJogador) VALUES 
('Toadette', 100, 10, 0, 1, 'Jogador'),
('Mario', 100, 10, 0, 1, 'Jogador'),
('Luigi', 100, 5, 0, 1, 'Jogador'),
('Donkey Kong', 100, 5, 0, 3, 'NPC'),
('Shy Guy', 100, 8, 0, 2, 'Inimigo'),
('Goomba', 30, 5, 0, 1, 'Inimigo'),
('Koopa Troopa', 40, 6, 0, 1, 'Inimigo'),
('Boo', 25, 12, 0, 2, 'Inimigo'),
('Thwomp', 50, 15, 0, 3, 'Inimigo'),
('Dry Bones', 35, 7, 0, 3, 'Inimigo'),
('Chain Chomp', 60, 12, 0, 3, 'Inimigo');


--- Insere inimigos na tabela Inimigo ---
INSERT INTO Inimigo (idPersonagem, tipo, habilidade) VALUES 
((SELECT idPersonagem FROM Personagem WHERE nome = 'Goomba'), 'Goomba', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Koopa Troopa'), 'Koopa Troopa', 'Defender'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Boo'), 'Boo', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Thwomp'), 'Thwomp', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Dry Bones'), 'Dry Bones', 'Defender'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Chain Chomp'), 'Chain Chomp', 'Atacar');

--- Insere lojas na tabela Loja ---
INSERT INTO Loja (nome) VALUES 
('Loja do Toad'),
('Loja do Yoshi'),
('Loja de Itens Raros');


--- Insere checkpoints na tabela Checkpoint ---
INSERT INTO Checkpoint (pontuação) VALUES 
(100),
(200),
(300);

-- Inserindo itens no inventário de um personagem (idPersonagem = 1)
INSERT INTO Inventario (quantidade, idItem, idPersonagem) VALUES 
(5, 1, 1),  -- 5 unidades do item com idItem = 1 para o personagem 1
(3, 2, 2),  -- 3 unidades do item com idItem = 2 para o personagem 1
(7, 3, 3);  -- 7 unidades do item com idItem = 3 para o personagem 1



--- Insere jogadores na tabela Jogador ---
INSERT INTO Jogador (moeda, idInventario, idYoshi) VALUES 
(100, (SELECT idInventario FROM Inventario WHERE idPersonagem = 1), 1),
(50, (SELECT idInventario FROM Inventario WHERE idPersonagem = 2), 2),
(75, (SELECT idInventario FROM Inventario WHERE idPersonagem = 3), 3);

--- Insere instâncias na tabela Instancia ---
INSERT INTO Instancia (vidaAtual, moedaAtual, idJogador) VALUES 
(40, 63, 1),
(70, 19, 2),
(90, 25, 3);
