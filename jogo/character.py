import curses
from db import connect_to_db

def get_characters_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT tipo FROM Jogador"
            cursor.execute(query)
            characters = [row[0] for row in cursor.fetchall()]
        return characters
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
        stdscr.addstr(i + 1, 0, f"[{i + 1}] {character}")

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
        
        if encounter == "Combat":
            stdcsr.addstr(0, 0, "Você encontrou inimigos! Se prepare para o combate.")
            mario_battle_turn(stdscr, player)  # Iniciar o jogo com o personagem escolhido
        elif encounter == "loja":
            stdcsr.addstr(0, 0, "Você encontrou uma loja!")
            stdcsr.addstr(0, 1, "[1] Comprar")
            stdcsr.addstr(0, 2, "[2] Vender")
        elif encounter == "blocos":
            stdcsr.addstr(0, 0, "Você encontrou uma blocos!")
            stdcsr.addstr(0, 1, "[1] Bater no bloco")
            stdcsr.addstr(0, 2, "[2] Ignora bloco")
        elif encounter == "cano":
            stdcsr.addstr(0, 0, "Você encontrou uma cano!")
            stdcsr.addstr(0, 1, "[1] Tentar entrar no cano")
            stdcsr.addstr(0, 2, "[2] Ignorar cano")
        elif encounter == "npc":
            stdcsr.addstr(0, 0, "Você encontrou um npc!")
            stdcsr.addstr(0, 1, "[1] Conversar com npc")
            stdcsr.addstr(0, 2, "[2] Ignorar npc")

        stdcsr.refresh()
        choice = stdcsr.getkey()

        if choice == "1":
            if encounter == "loja":
                print("Fazer interação de comprar algo da loja")
            elif encounter == "blocos":
                print("Fazer interação de bater no bloco")
            elif encounter == "cano":
                print("Fazer interação de entrar no cano")
            elif encounter == "npc":
                print("Fazer interação de conversar com npc")
        elif choice == "1":
            if encounter == "loja":
                print("Fazer interação de vender algo da loja")
            elif encounter == "blocos":
                print("Fazer interação de ignorar bloco")
            elif encounter == "cano":
                print("Fazer interação de ignorar cano")
            elif encounter == "npc":
                print("Fazer interação de ignorar npc")
        else:
            stdcsr.addstr(4, 0, "Escolha inválida. Tente novamente.")

        stdcsr.refresh()
        stdcsr.gettch()