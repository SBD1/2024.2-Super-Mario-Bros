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

--- Insere blocos na tabela Bloco ---
INSERT INTO Bloco (tipo) VALUES 
('Bloco de Yoshi'),
('Bloco de Moedas'),
('Bloco de Vida Extra'),
('Bloco de Cogumelo'),
('Bloco de Flor de Fogo'),
('Bloco de Estrela');

-- Insere locais na tabela Local para cada fase
INSERT INTO Local (nome, regiao, descricao, idFase, idBloco, idPersonagem, idLoja, idCheckpoint) VALUES
('Castelo do Bowser', 'norte', 'Um castelo cheio de lava e armadilhas.', 3, 1, NULL, NULL, NULL),
('Campos do Reino', 'oeste', 'Um campo verde com muitos Goombas.', 1, 2, NULL, NULL, NULL),
('Caverna Aquática', 'sul', 'Um local submerso com peixes hostis.', 2, 3, NULL, NULL, NULL),
('Deserto das Dunas', 'oeste', 'Um vasto deserto cheio de armadilhas.', 3, 4, NULL, NULL, NULL),
('Floresta Perdida', 'norte', 'Uma floresta cheia de segredos ocultos.', 2, NULL, 2, NULL, NULL),
('Montanhas Congeladas', 'leste', 'Um local coberto de neve e gelo.', 1, 5, NULL, NULL, NULL),
('Praia Ensolarada', 'leste', 'Um local relaxante com perigos inesperados.', 3, NULL, 10, NULL, NULL);


--- Insere personagens na tabela Personagem ---
INSERT INTO Personagem (nome, vida, dano, pontos, idLocal, tipoJogador) VALUES 
('Toadette', 100, 10, 0, 6, 'Jogador'),
('Mario', 100, 10, 0, 6, 'Jogador'),
('Luigi', 100, 5, 0, 3, 'Jogador'),
('Donkey Kong', 100, 5, 0, 3, 'NPC'),
('Shy Guy', 100, 8, 0, 2, 'Inimigo'),
('Goomba', 30, 5, 0, 1, 'Inimigo'),
('Koopa Troopa', 40, 6, 0, 1, 'Inimigo'),
('Boo', 25, 4, 0, 1, 'Inimigo'),
('Thwomp', 50, 10, 0, 1, 'Inimigo'),
('Dry Bones', 35, 7, 0, 1, 'Inimigo'),
('Chain Chomp', 60, 12, 0, 1, 'Inimigo'),
('Boohemoth', 70, 15, 0, 1, 'Inimigo');


--- Insere inimigos na tabela Inimigo ---
INSERT INTO Inimigo (idPersonagem, tipo, habilidade) VALUES 
((SELECT idPersonagem FROM Personagem WHERE nome = 'Goomba'), 'Goomba', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Koopa Troopa'), 'Koopa Troopa', 'Defender'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Boo'), 'Boo', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Thwomp'), 'Thwomp', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Dry Bones'), 'Dry Bones', 'Defender'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Chain Chomp'), 'Chain Chomp', 'Atacar'),
((SELECT idPersonagem FROM Personagem WHERE nome = 'Boohemoth'), 'Boohemoth', 'Atacar');

--- Insere itens na tabela Item ---
INSERT INTO Item (tipo, efeito, duração, raridade) VALUES 
('Cogumelo', 'Aumenta tamanho', 60, 'Comum'),
('Flor de Fogo', 'Atira bolas de fogo', 30, 'Raro'),
('Estrela', 'Invencibilidade', 10, 'Muito Raro');



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

--- Insere inventários na tabela Inventario ---
INSERT INTO Inventario (quantidade, idItem) VALUES 
(5, 1),
(3, 2),
(7, 3);


--- Insere jogadores na tabela Jogador ---
INSERT INTO Jogador (moeda, idInventario, idYoshi) VALUES 
(100, 1, 1),
(50, 2, 2),
(75, 3, 3);

--- Insere instâncias na tabela Instancia ---
INSERT INTO Instancia (vidaAtual, moedaAtual, idJogador) VALUES 
(40, 63, 1),
(70, 19, 2),
(90, 25, 3);
