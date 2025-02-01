import curses
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
        
def player_turn(stdcsr, player, encounter):
    while True:
        stdcsr.clear()
        row = 0

        if encounter.get('Personagem') is not None:
            if encounter.get('Personagem').get('tipo') == 'NPC':
                stdcsr.addstr(row, 0, "Você encontrou um NPC")
                row += 1
                stdcsr.addstr(row, 0, "[1] Conversar")
                row += 1
                stdcsr.addstr(row, 0, "[2] Ignorar")
            else:
                stdcsr.addstr(row, 0, "Você encontrou inimigos! Se prepare para o combate.")
                stdcsr.refresh()
                stdcsr.getch() 
                mario_battle_turn(stdcsr, player)

        row += 1  # Avança a linha

        if encounter.get('Loja') is not None:
            stdcsr.addstr(row, 0, "Você encontrou uma loja!")
            row += 1
            stdcsr.addstr(row, 0, "[1] Comprar")
            row += 1
            stdcsr.addstr(row, 0, "[2] Vender")

        if encounter.get('Bloco') is not None:
            stdcsr.addstr(row, 0, "Você encontrou um bloco!")
            row += 1
            stdcsr.addstr(row, 0, "[1] Bater no bloco")
            row += 1
            stdcsr.addstr(row, 0, "[2] Ignorar bloco")

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
    