import curses
import battle
from db import connect_to_db
from battle import mario_battle_turn

class Character:
    def __init__(self, id_character, name, vida):
        self.id = id_character
        self.name = name
        self.vida = vida

def get_characters_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.idpersonagem, p.nome, p.vida, p.dano, p.pontos, p.idLocal, p.tipojogador
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
                vida=character[2]
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
        elif moeda:
            item_name = f"{moeda} moedas"
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
    """Retorna os itens do inventário de um jogador."""
    connection = connect_to_db()
    if not connection:
        return "Erro ao conectar ao banco de dados."

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT i.tipo, i.efeito, i.duração, i.raridade, inv.quantidade
            FROM Inventario inv
            JOIN Item i ON inv.idItem = i.idItem
            WHERE inv.idPersonagem = %s
            """
            cursor.execute(query, (player_id,))
            items = cursor.fetchall()

        if not items:
            return "Seu inventário está vazio."

        return items

    except Exception as e:
        return f"Erro ao buscar itens do inventário: {e}"
    finally:
        connection.close()

def player_turn(stdscr, player, encounter):
    while True:
        stdscr.clear()  # Limpa a tela a cada novo turno
        row = 0

        # Exibe detalhes do encontro
        if encounter.get('Personagem') is not None:
            if encounter.get('Personagem').get('tipo') == 'NPC':
                stdscr.addstr(row, 0, "Você encontrou um NPC")
                row += 1
                stdscr.addstr(row, 0, "[1] Conversar")
                row += 1
                stdscr.addstr(row, 0, "[2] Ignorar")
            else:
                stdscr.addstr(row, 0, "Você encontrou inimigos! Se prepare para o combate.")
                stdscr.refresh()
                stdscr.getch() 
                mario_battle_turn(stdscr, player)

        row += 1  # Avança a linha

        if encounter.get('Loja') is not None:
            stdscr.addstr(row, 0, "Você encontrou uma loja!")
            row += 1
            stdscr.addstr(row, 0, "[1] Comprar")
            row += 1
            stdscr.addstr(row, 0, "[2] Vender")

        if encounter.get('Bloco') is not None:
            stdscr.addstr(row, 0, "Você encontrou um bloco!")
            row += 1
            stdscr.addstr(row, 0, "[1] Bater no bloco")
            row += 1
            stdscr.addstr(row, 0, "[2] Ignorar bloco")
            stdscr.refresh()

            choice = stdscr.getkey()

        if choice == "1":  # Jogador escolheu bater no bloco
            stdscr.clear()  # Limpa a tela para a próxima mensagem
            stdscr.addstr(row + 1, 0, "Você bateu no bloco!")
            stdscr.refresh()
            stdscr.getch()  # Pausa para dar efeito

            item_description = get_block_item(encounter.get('Bloco'), player)  # Obtém o item do bloco e adiciona ao inventário
            
            if item_description:
                stdscr.clear()  # Limpa a tela antes de mostrar a próxima mensagem
                stdscr.addstr(row + 3, 0, f"Você encontrou: {item_description}!")
                row += 1
            else:
                stdscr.addstr(row + 3, 0, "O bloco estava vazio.")

            # Exibindo os itens no inventário após o item do bloco ser encontrado
            stdscr.addstr(row + 4, 0, "Itens no seu inventário:")
            inventory_items = get_inventory_items(player.id)
            if isinstance(inventory_items, list):
                for i, item in enumerate(inventory_items):
                    stdscr.addstr(row + 5 + i, 0, f"{item[0]} (Efeito: {item[1]}) - {item[4]} unidades")
            else:
                stdscr.addstr(row + 5, 0, inventory_items)

            stdscr.refresh()
            stdscr.getch()  # Espera o jogador pressionar uma tecla antes de continuar

            stdscr.clear()  # Limpa a tela antes de mostrar a batalha
            stdscr.addstr(row + 6, 0, "Prepare-se para a batalha!")
            stdscr.refresh()
            stdscr.getch()  # Pausa para dar um pouco de tempo

            # Chama a função de batalha
            battle.mario_battle_turn(stdscr, player)


        
        elif choice == "2":  # Jogador escolheu ignorar o bloco
            stdscr.clear()  # Limpa a tela antes de mostrar a mensagem de ignorar
            stdscr.addstr(row + 1, 0, "Você ignorou o bloco.")
            stdscr.refresh()
            stdscr.getch()
            return

        # Ação de checkpoint e outras interações seguem aqui...

        stdscr.refresh()
        stdscr.getch()  # Esperar jogador pressionar tecla antes de limpar e repetir loop        

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

       
        if encounter.get('CheckPoint!') is not None:
            stdcsr.addstr(row, 0, "Você encontrou um CheckPoint!")
            row += 1
            stdcsr.addstr(row, 0, "CheckPoint Ativado!")
            active_checkpoint(player)  # Ativa o checkpoint para o jogador

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

def active_checkpoint(player):
    player.last_checkpoint = player.position.copy()  # Salva a posição do jogador no último checkpoint
    player.health = player.max_health  # Restaura o hp completo do jogador
    