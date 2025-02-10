import curses
import pygame
from battle import exibir_mapa
from matriz import gera_matriz
from db import connect_to_db
from battle import turno_batalha
from loja import get_loja_with_items, comprar_item, vender_item, Item
import random

pygame.init()

pygame.mixer.init()

class Character:
    def __init__(self, id_character, name, vida, dano, pontos, id_local, tipo_jogador, moeda):
        self.id = id_character
        self.name = name
        self.vida = vida
        self.dano = dano
        self.pontos = pontos
        self.id_local = id_local
        self.tipo_jogador = tipo_jogador
        self.moeda = moeda
        self.posicao = [1, 1]
        self.mapa = None 

    def gerar_posicao_aleatoria(self, mapa):
        while True:
            x = random.randint(0, len(mapa) - 1)
            y = random.randint(0, len(mapa[0]) - 1)
            if mapa[x][y] != 'M':  # Garantir que a posição não seja ocupada pelo Mario
                return [x, y]

    def mover(self, direcao, mapa):
        nova_posicao = self.posicao[:]
        
        if direcao == "UP":
            nova_posicao[0] -= 1
        elif direcao == "DOWN":
            nova_posicao[0] += 1
        elif direcao == "LEFT":
            nova_posicao[1] -= 1
        elif direcao == "RIGHT":
            nova_posicao[1] += 1

        # Verifica se a nova posição está dentro dos limites da matriz
        if 0 <= nova_posicao[0] < len(mapa) and 0 <= nova_posicao[1] < len(mapa[0]):
            self.posicao = nova_posicao
            print(f"Mario se moveu para {self.posicao}")
            
            # Verifica se Mario passou pela posição do checkpoint
            if self.posicao == self.checkpoint and not self.salvou_checkpoint:
                self.salvou_checkpoint = True
                print("Checkpoint salvo!")
                curses.napms(1000)  # Espera 2 segundos para dar tempo de ver a mensagem
        else:
            print("Movimento inválido!")

    def atacar(self, item, inimigo):
        dano = item.dano
        
        if dano > 0:
            inimigo.perder_vida(dano)
            return dano
        return 0

    def desviar(self, mapa):
        # Marca a posição atual de Mario com "I" antes de mudar de posição
        mapa[self.posicao[0]][self.posicao[1]] = 'I'
        
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Representando movimentos de 1 casa

        # Coordenadas atuais de Mario
        x, y = self.posicao

        # Tentativa de desviar até encontrar uma casa válida
        while True:
            # Escolher uma direção aleatória
            direcao = random.choice(direcoes)

            # Calcular nova posição
            nova_posicao = [x + direcao[0], y + direcao[1]]

            # Verificar se a nova posição está dentro dos limites do mapa e não é [7,7]
            if 0 <= nova_posicao[0] < len(mapa) and 0 <= nova_posicao[1] < len(mapa[0]) and nova_posicao != [7, 7]:
                self.posicao = nova_posicao  # Atualizar posição de Mario
                break  # Sair do loop quando encontrar uma posição válida

    def pular(self, inimigo):
        print("Mario pula para atacar o inimigo!")
        
        # O dano do pulo é menor e causa dano instantâneo no Goomba
        dano_pulo = 10
        if inimigo.nome == "Goomba":
            inimigo.perder_vida(inimigo.vida)  # Goomba morre instantaneamente
            print(f"Goomba foi derrotado instantaneamente!")
        else:
            inimigo.perder_vida(dano_pulo)
            print(f"{inimigo.nome} sofreu {dano_pulo} de dano pelo pulo!")

class Inimigo:
    def __init__(self, nome, vida, dano, pontos, id_local, tipo, habilidade, mapa):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.pontos = pontos
        self.id_local = id_local
        self.tipo = tipo
        self.habilidade = habilidade
        self.posicao = self.gerar_posicao_aleatoria(mapa)  # Posição aleatória para o inimigo
        self.derrotado = False  # Indica se o inimigo foi derrotado

    def gerar_posicao_aleatoria(self, mapa):
        while True:
            x = random.randint(0, len(mapa) - 1)
            y = random.randint(0, len(mapa[0]) - 1)
            if mapa[x][y] != 'M' and mapa[x][y] != 'C':  # Garantir que a posição não seja ocupada por Mario ou pelo checkpoint
                return [x, y]

    def atacar(self):
        return self.dano

    def perder_vida(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.derrotado = True  # Marca como derrotado quando a vida chegar a zero

def get_characters_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.idpersonagem, p.nome, p.vida, p.dano, p.pontos, p.idFase, p.tipojogador, j.moeda
            FROM personagem p
            JOIN jogador j ON p.idpersonagem = j.idpersonagem
            WHERE p.tipojogador = 'Jogador'
            """
            cursor.execute(query)
            characters = cursor.fetchall()

        if not characters:
            return "Nenhum jogador disponível para escolha."

        characters_list = [
            Character(
                id_character=character[0],
                name=character[1], 
                vida=character[2],
                dano=character[3],
                pontos=character[4],
                id_local=character[5],
                tipo_jogador=character[6],
                moeda=character[7]
            )
            for character in characters
        ]
    
        return characters_list
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def get_inimigo_from_db(id_personagem, mapa):
    """Retorna um objeto Inimigo do banco de dados com base no idPersonagem."""
    connection = connect_to_db()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.nome, p.vida, p.dano, p.pontos, p.idFase, i.tipo, i.habilidade
            FROM Personagem p
            JOIN Inimigo i ON p.idPersonagem = i.idPersonagem
            WHERE p.idPersonagem = %s AND p.tipoJogador = 'Inimigo'
            """
            cursor.execute(query, (id_personagem,))
            inimigo_data = cursor.fetchone()

        if not inimigo_data:
            return None  # Retorna None se o inimigo não for encontrado

        # Criando e retornando um objeto Inimigo
        return Inimigo(
            nome=inimigo_data[0],
            vida=inimigo_data[1],
            dano=inimigo_data[2],
            pontos=inimigo_data[3],
            id_local=inimigo_data[4],
            tipo=inimigo_data[5],
            habilidade=inimigo_data[6],
            mapa=mapa
        )

    except Exception as e:
        print(f"Erro ao buscar inimigo: {e}")
        return None
    finally:
        connection.close()

def choose_character(stdscr):
    """Exibe a tela para o jogador escolher o personagem."""

    characters = get_characters_from_db()

    if not characters:
        stdscr.addstr(0, 0, "Nenhum personagem disponível no banco de dados!")
        stdscr.refresh()
        stdscr.getch()
        return None

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha seu personagem:")

    for i, character in enumerate(characters):
        stdscr.addstr(i + 1, 0, f"[{i + 1}] {character.name} - Vida: {character.vida}")

    stdscr.addstr(len(characters) + 2, 0, "Pressione o número correspondente para escolher.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(characters):
            chosen_index = key - ord('1')
            return characters[chosen_index]
        
def get_block_item(id_bloco, player):
    """Retorna o item escondido dentro de um bloco e o adiciona ao inventário do jogador."""
    connection = connect_to_db()
    if not connection:
        return "Erro ao conectar ao banco de dados."

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT 
                i.idItem AS id_item,  -- Agora retornando o idItem
                i.tipo AS item, 
                y.nome AS yoshi, 
                m.valor AS moeda 
            FROM Bloco b
            LEFT JOIN Item i ON b.idItem = i.idItem
            LEFT JOIN Yoshi y ON b.idYoshi = y.idYoshi
            LEFT JOIN Moeda m ON b.idMoeda = m.idMoeda
            WHERE b.idBloco = %s
            """
            cursor.execute(query, (id_bloco,))
            result = cursor.fetchone()

        if not result:
            return "O bloco está vazio."

        id_item, item, yoshi, moeda = result
        if item:
            item_name = item
        elif yoshi:
            item_name = f"Yoshi: {yoshi}"
            with connection.cursor() as cursor:
                update_yoshi_query = """
                UPDATE Jogador
                SET idYoshi = %s
                WHERE idPersonagem = %s
                """
                cursor.execute(update_yoshi_query, (yoshi, player.id)) 
                connection.commit()
        elif moeda:
            item_name = f"{moeda} moedas"
            player.moeda += moeda
            with connection.cursor() as cursor:
                check_query = """
                SELECT moeda
                FROM Jogador
                WHERE idPersonagem = %s
                """
                cursor.execute(check_query, (player.id,))
                current_money = cursor.fetchone()

                if current_money:
                    new_money = current_money[0] + moeda
                    update_money_query = """
                    UPDATE Jogador
                    SET moeda = %s
                    WHERE idPersonagem = %s
                    """
                    cursor.execute(update_money_query, (new_money, player.id))
                    connection.commit()
                else:
                    insert_money_query = """
                    UPDATE Jogador
                    SET moeda = %s
                    WHERE idPersonagem = %s
                    """
                    cursor.execute(insert_money_query, (moeda, player.id))
                    connection.commit()
        else:
            return "O bloco está vazio."

        # Definir a quantidade inicial (supondo que seja 1)
        quantidade = 1

        # Adiciona o idItem e a quantidade ao inventário do jogador
        with connection.cursor() as cursor:
            # Verifica se o jogador já possui o item no inventário
            check_query = """
            SELECT idInventario, quantidade
            FROM Inventario
            WHERE idItem = %s AND idpersonagem = %s
            """
            cursor.execute(check_query, (id_item, player.id))  # Garanta que 'player.id' esteja correto
            existing_item = cursor.fetchone()

            if existing_item:
                # Se já existe, atualiza a quantidade
                new_quantity = existing_item[1] + quantidade
                update_query = """
                UPDATE Inventario
                SET quantidade = %s
                WHERE idInventario = %s
                """
                cursor.execute(update_query, (new_quantity, existing_item[0]))
            else:
                # Se não existe, insere o novo item no inventário
                insert_query = """
                INSERT INTO Inventario (quantidade, idItem, idpersonagem)
                VALUES (%s, %s, %s)  -- Aqui garantimos que 'idpersonagem' seja passado
                """
                cursor.execute(insert_query, (quantidade, id_item, player.id))  # Insira o id do personagem aqui

            connection.commit()

        return f" {item_name}!"

    except Exception as e:
        return f"Erro ao buscar item do bloco: {e}"
    finally:
        connection.close()

def get_inventory_items(player_id):
    """Retorna os itens do inventário de um jogador no formato da classe Item."""
    connection = connect_to_db()
    if not connection:
        return "Erro ao conectar ao banco de dados."

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT i.idItem, i.tipo, i.efeito, i.duração, i.raridade, inv.quantidade
            FROM Inventario inv
            JOIN Item i ON inv.idItem = i.idItem
            WHERE inv.idPersonagem = %s
            """
            cursor.execute(query, (player_id,))
            items_data = cursor.fetchall()

        if not items_data:
            return "Seu inventário está vazio."

        inventory_items = [
            Item(id_item, tipo, efeito, duracao, raridade, quantidade)
            for id_item, tipo, efeito, duracao, raridade, quantidade in items_data
        ]

        return inventory_items

    except Exception as e:
        return f"Erro ao buscar itens do inventário: {e}"
    finally:
        connection.close()


# def player_turn(stdscr, player, encounter):
#     mapa = None  # Inicializa a variável antes de usá-la

#     while True:
#         stdscr.clear()  # Limpa a tela a cada novo turno
#         row = 0

#         # Exibe detalhes do encontro
#         if encounter.get('Personagem') is not None:
#             if encounter.get('Personagem').get('tipo') == 'NPC':
#                 stdscr.addstr(row, 0, "Você encontrou um NPC")
#                 row += 1
#                 stdscr.addstr(row, 0, "[1] Conversar")
#                 row += 1
#                 stdscr.addstr(row, 0, "[2] Ignorar")
#             if encounter.get('Personagem').get('tipo') == 'Inimigo':
#                 stdscr.addstr(row, 0, "Você encontrou inimigos! Se prepare para o combate.")
#                 stdscr.refresh()
#                 stdscr.getch() 

#                 mapa = gera_matriz(linhas=8, colunas=8)
#                 items = get_inventory_items(player.id)
#                 inimigo = get_inimigo_from_db(encounter.get('Personagem').get('id'), items)
#                 turno_batalha(stdscr, player, inimigo, mapa, items)

#         row += 1  # Avança a linha

#         if encounter.get('Loja') is not None:
#             stdscr.addstr(row, 0, "Você encontrou uma loja!")
#             row += 1
#             stdscr.addstr(row, 0, "[1] Comprar")
#             row += 1
#             stdscr.addstr(row, 0, "[2] Vender")

#             choice = stdscr.getkey()

#         if encounter.get('Bloco') is not None:
#             stdscr.addstr(row, 0, "Você encontrou um bloco!")
#             row += 1
#             stdscr.addstr(row, 0, "[1] Bater no bloco")
#             row += 1
#             stdscr.addstr(row, 0, "[2] Ignorar bloco")
#             stdscr.refresh()

#             choice = stdscr.getkey()

#         if encounter.get('CheckPoint!') is not None:
#             stdscr.addstr(row, 0, "Você encontrou um CheckPoint!")
#             row += 1
#             stdscr.addstr(row, 0, "CheckPoint Ativado!")
#             active_checkpoint(player)

#         if choice == "1" and encounter.get('Bloco') is not None:  # Jogador escolheu bater no bloco
#             stdscr.clear()  # Limpa a tela para a próxima mensagem
#             stdscr.addstr(row + 1, 0, "Você bateu no bloco!")
#             stdscr.refresh()
#             stdscr.getch()  # Pausa para dar efeito

#             item_description = get_block_item(encounter.get('Bloco'), player)  # Obtém o item do bloco e adiciona ao inventário
            
#             if item_description:
#                 stdscr.clear()  # Limpa a tela antes de mostrar a próxima mensagem
#                 stdscr.addstr(row + 3, 0, f"Você encontrou: {item_description}!")
#                 row += 1
#             else:
#                 stdscr.addstr(row + 3, 0, "O bloco estava vazio.")

#             # Exibindo os itens no inventário após o item do bloco ser encontrado
#             stdscr.addstr(row + 4, 0, "Itens no seu inventário:")
#             inventory_items = get_inventory_items(player.id)
#             if isinstance(inventory_items, list):
#                 for i, item in enumerate(inventory_items):
#                     stdscr.addstr(row + 5 + i, 0, f"{item.tipo} (Efeito: {item.efeito}) - {item.quantidade} unidades")
#             else:
#                 stdscr.addstr(row + 5, 0, inventory_items)

#             stdscr.refresh()
#             stdscr.getch()  # Espera o jogador pressionar uma tecla antes de continuar

#             stdscr.clear()  # Limpa a tela antes de mostrar a batalha
#             stdscr.addstr(row + 6, 0, "Prepare-se para a batalha!")
#             stdscr.refresh()
#             stdscr.getch()  # Pausa para dar um pouco de tempo

#             mapa = exibir_mapa(stdscr, player, mapa)
#             # Pegando o mapa
#             music_channel = pygame.mixer.Channel(0)

#             # Chama a função de batalha
#             turno_batalha(stdscr, player, inimigo, mapa, music_channel)

#         elif choice == "2" and encounter.get('Bloco') is not None:  # Jogador escolheu ignorar o bloco
#             stdscr.clear()  # Limpa a tela antes de mostrar a mensagem de ignorar
#             stdscr.addstr(row + 1, 0, "Você ignorou o bloco.")
#             stdscr.refresh()
#             stdscr.getch()
#             return
        
#         if choice == "1" and encounter.get('Loja') is not None:
#             loja = get_loja_with_items(encounter.get('Loja'))
#             comprar_item(stdscr, player, loja)
#         elif choice == "2" and encounter.get('Loja') is not None:
#             loja = get_loja_with_items(encounter.get('Loja'))
#             vender_item(stdscr, player.id, loja)

        
#         # Ação de checkpoint e outras interações seguem aqui...

#         stdscr.refresh()
#         stdscr.getch()  # Esperar jogador pressionar tecla antes de limpar e repetir loop        

def insert_item_into_inventory(player_id, item_id, quantity):
        connection = connect_to_db()
        if not connection:
            return "Erro ao conectar ao banco de dados."

        try:
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO Inventario (quantidade, idItem, idpersonagem)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (quantity, item_id, player_id))
                connection.commit()
                return "Item adicionado ao inventário com sucesso!"

        except Exception as e:
            connection.rollback()  # Caso ocorra algum erro, desfaça a transação
            return f"Erro ao adicionar item ao inventário: {e}"

        finally:
            connection.close()


        stdcsr.refresh()
        choice = stdcsr.getkey()

        if choice == "1":
            if encounter.get('Loja') is not None:
                stdcsr.addstr(row + 2, 0, "Você escolheu comprar algo da loja.")
                itens = get_shop_itens(encounter.get('Loja'))

            elif encounter.get('Bloco') is not None:
                stdcsr.addstr(row + 2, 0, "Você bateu no bloco.")
                item = get_block_item(encounter.get('Bloco'))

        elif choice == "2":
            if encounter.get('Loja') is not None:
                stdcsr.addstr(row + 2, 0, "Você escolheu vender algo da loja.")
                itens = get_inventario_itens(player.id)
                # Fazer a interação de tirar o item do inventário e vender para ganhar moedas
            elif encounter.get('Bloco') is not None:
                stdcsr.addstr(row + 2, 0, "Você ignorou o bloco.")

        else:
            stdcsr.addstr(row + 2, 0, "Escolha inválida. Tente novamente.")

        stdcsr.refresh()
        stdcsr.getch()  # Esperar jogador pressionar tecla antes de limpar e repetir loop

# def active_checkpoint(player):
#     player.last_checkpoint = player.position.copy()  # Salva a posição do jogador no último checkpoint
#     player.health = player.max_health  # Restaura o hp completo do jogador
    