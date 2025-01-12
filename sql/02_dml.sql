-- Conecta ao banco supermario
\c supermario;

--- Insere inimigos na tabela Inimigo ---
INSERT INTO Inimigo (tipo) VALUES 
('Goomba'),
('Koopa Troopa'),
('Boo'),
('Thwomp'),
('Dry Bones'),
('Chain Chomp'),
('Boohemoth');

--- Insere canos na tabela Cano ---
INSERT INTO Cano (idDestino) VALUES 
('Mundo 1-1'),
('Mundo 2-2'),
('Mundo 3-3');

--- Insere mundos na tabela Mundo ---
INSERT INTO Mundo (nome, descrição, nivel, idCano) VALUES 
('Mundo 1', 'Um mundo inicial cheio de novas aventuras.', 1, 1),
('Mundo 2', 'Um mundo aquático cheio de dificuldades.', 2, 2),
('Mundo 3', 'Um mundo de lava com perigos por todos os lados.', 3, 3);

--- Insere fases na tabela Fase ---
INSERT INTO Fase (nome, nivel, idMundo) VALUES 
('Fase 1', 1, 1),
('Fase 2', 2, 2),
('Fase 3', 3, 3);

--- Insere locais na tabela Local para cada fase ---
INSERT INTO Local (nome, descricao, idFase) VALUES 
('Castelo do Bowser', 'Um castelo cheio de lava e armadilhas.', 3),
('Campos do Reino', 'Um campo verde com muitos Goombas.', 1),
('Caverna Aquática', 'Um local submerso com peixes hostis.', 2),
('Deserto das Dunas', 'Um vasto deserto cheio de armadilhas.', 3),
('Floresta Perdida', 'Uma floresta cheia de segredos ocultos.', 2),
('Montanhas Congeladas', 'Um local coberto de neve e gelo.', 1),
('Praia Ensolarada', 'Um local relaxante com perigos inesperados.', 3);

--- Insere blocos na tabela Bloco ---
INSERT INTO Bloco (tipo, idLocal) VALUES 
('Bloco de Yoshi', 1),
('Bloco de Moedas', 2),
('Bloco de Vida Extra', 1),
('Bloco de Cogumelo', 3),
('Bloco de Yoshi', 2),
('Bloco de Moedas', 5),
('Bloco de Moedas', 6),
('Bloco de Flor de Fogo', 4),
('Bloco de Yoshi', 7),
('Bloco de Estrela', 4);

--- Insere Yoshis na tabela Yoshi ---
INSERT INTO Yoshi (nome, idBloco) VALUES 
('Yoshi Verde', 5),
('Yoshi Azul', 9),
('Yoshi Vermelho', 1);

--- Insere moedas na tabela Moeda ---
INSERT INTO Moeda (valor, idBloco) VALUES 
(1, 2),
(5, 6),
(10, 7);

--- Insere lojas na tabela Loja ---
INSERT INTO Loja (nome, idLocal) VALUES 
('Loja do Toad', 3),
('Loja do Yoshi', 5),
('Loja de Itens Raros', 7);

--- Insere itens na tabela Item ---
INSERT INTO Item (tipo, efeito, duração, raridade, idBloco) VALUES 
('Cogumelo', 'Aumenta tamanho', 60, 'Comum', 4),
('Flor de Fogo', 'Atira bolas de fogo', 30, 'Raro', 8),
('Estrela', 'Invencibilidade', 10, 'Muito Raro', 10);

--- Insere personagens na tabela Personagem ---
INSERT INTO Personagem (nome, vida, dano, pontos, idLocal) VALUES 
('Toadette', 100, 10, 0, 6),
('Shy Guy', 100, 8, 0, 2),
('Donkey Kong', 100, 5, 0, 3);

--- Insere checkpoints na tabela Checkpoint ---
INSERT INTO Checkpoint (pontuação, idLocal) VALUES 
(100, 6),
(200, 3),
(300, 7);

--- Insere inventários na tabela Inventario ---
INSERT INTO Inventario (quantidade, IdItem) VALUES 
(5, 1),
(3, 2),
(7, 3);

--- Insere jogadores na tabela Jogador ---
INSERT INTO Jogador (tipo, moeda, idInventario, idYoshi) VALUES 
('Mario', 100, 1, 1),
('Luigi', 50, 2, 2),
('Peach', 75, 3, 3);

--- Insere instâncias na tabela Instancia ---
INSERT INTO Instancia (vidaAtual, moedaAtual, idJogador) VALUES 
(40, 63, 1),
(70, 19, 2),
(90, 25, 3);