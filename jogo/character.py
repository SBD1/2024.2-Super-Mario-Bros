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

import random
import curses  # Certifique-se de que o módulo curses esteja importado se você estiver usando-o

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
        self.checkpoint = [1, 1]  # Inicializa o checkpoint na mesma posição inicial
        self.salvou_checkpoint = False  # Inicializa a flag que verifica se o checkpoint foi salvo
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
            # print(f"Mario se moveu para {self.posicao}")
            
            # Verifica se Mario passou pela posição do checkpoint
            if self.posicao == self.checkpoint and not self.salvou_checkpoint:
                self.salvou_checkpoint = True
                print("Checkpoint salvo!")
                curses.napms(1000)  # Espera 1 segundo para dar tempo de ver a mensagem
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
        
def get_block_item(encounter, player):
    """Retorna o item escondido dentro de um bloco e o adiciona ao inventário do jogador."""
    connection = connect_to_db()
    if not connection:
        return "Erro ao conectar ao banco de dados."

    try:
        # Verifica se `encounter` é um objeto Bloco e extrai o ID do bloco
        if hasattr(encounter, 'id_bloco'):
            id_bloco = encounter.id_bloco
        else:
            return "Erro: O objeto 'encounter' não é um Bloco válido."

        with connection.cursor() as cursor:
            query = """
            SELECT 
                i.idItem AS id_item,  -- Agora retornando o idItem
                i.tipo AS item,
                y.idYoshi as id_yoshi, 
                y.nome AS yoshi,
                m.valor AS moeda 
            FROM Bloco b
            LEFT JOIN Item i ON b.idItem = i.idItem
            LEFT JOIN Yoshi y ON b.idYoshi = y.idYoshi
            LEFT JOIN Moeda m ON b.idMoeda = m.idMoeda
            WHERE b.idBloco = %s
            """
            cursor.execute(query, (id_bloco,))  # Passa o ID do bloco como um valor primitivo
            result = cursor.fetchone()

        if not result:
            return "O bloco está vazio."

        id_item, item, id_yoshi, yoshi, moeda = result
        if item:
            item_name = item
            
            quantidade = 1

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
        elif yoshi:
            item_name = f"Yoshi: {yoshi}"
            with connection.cursor() as cursor:
                update_yoshi_query = """
                UPDATE Jogador
                SET idYoshi = %s
                WHERE idPersonagem = %s
                """
                cursor.execute(update_yoshi_query, (id_yoshi, player.id)) 
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



# def active_checkpoint(player):
#     player.last_checkpoint = player.position.copy()  # Salva a posição do jogador no último checkpoint
#     player.health = player.max_health  # Restaura o hp completo do jogador
    