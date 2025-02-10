import curses
import time

from db import connect_to_db


class Mundo:
    def __init__(self, id_mundo, name, descricao, nivel):
        self.id_mundo = id_mundo
        self.name = name
        self.descricao = descricao
        self.nivel = nivel



def get_world_from_db():
    """Recupera os mundos do banco de dados."""
    connection = connect_to_db()
    if not connection:
        return []
    try:
        with connection.cursor() as cursor:

            query = "SELECT DISTINCT idMundo, nome, descrição, nivel FROM Mundo ORDER BY nivel"
            cursor.execute(query)
            worlds = [Mundo(id_mundo=row[0], name=row[1], descricao=row[2], nivel=row[3]) for row in cursor.fetchall()]
        return worlds
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()

def draw_ascii_art(stdscr, world):
    """Desenha uma arte ASCII correspondente ao mundo selecionado"""
    stdscr.clear()

    ascii_arts = {
        1:  [
        "       ^^   ^^         ",
        "     ^^  ^^  ^^       ",
        "    |  |   |  |    ",
        "    |__|___|__|     ",
        "    /          \\    ",  
        "   /    ____    \\   ",  
        "  /    |    |    \\  ",  
        " /_____|____|_____\\ ",
        "",
        "Bem-vindo ao mundo aventureiro!"
    ],
        2: [
        "            |    |    ",
        "           )_)  )_)  )_) ",
        "          )___))___))___)\\ ",
        "        )____)____)_____)\\\\ ",
        "      _____|____|____|____\\\\__ ",
        "------\\                   /------- ",
        "  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^^^^  ",
        "    ^^^^      ^^^^     ^^^^    ^^  ",
        "         ^^^^      ^^^^             ",
        "", 
        "Bem-vindo ao mundo aquático!"
    ],
        3: [
            "          ^    ^     ^          ",
            "         /\\   / \\   /\\         ",
            "        /  \\ /   \\ /  \\        ",
            "       /    \\     /    \\       ",
            "      /  ~~   ~~   ~~   \\      ",
            "     / ~~~~~ ~~~~~ ~~~~~ \\     ",
            "    /~~~~~~~~~~~~~~~~~~~~~\\    ",
            "   /~~~~~~~~~~~~~~~~~~~~~~~\\   ",
            "  /~~~~~~~~~~~~~~~~~~~~~~~~~\\  ",
            " /~~~~~~~~~~~~~~~~~~~~~~~~~~~\\ ",
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
            "", 
            "  Bem-vindo ao mundo vulcânico!  "
        ]
    }

    stdscr.addstr(1, 5, f"Você escolheu o {world.name}", curses.A_BOLD)
    for i, line in enumerate(ascii_arts.get(world.nivel, [])):
        stdscr.addstr(i + 3, 10, line, curses.color_pair(world.nivel) | curses.A_BOLD)
    
    stdscr.refresh()
    time.sleep(3)

def choose_world(stdscr):
    """Exibe a tela para o jogador escolher um mundo."""
    
    worlds = get_world_from_db()

    if not worlds:
        stdscr.addstr(0, 0, "Nenhum mundo disponível no banco de dados!", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return None

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.addstr(0, 0, "🌎 Escolha um mundo para entrar:", curses.A_BOLD)

    for i, world in enumerate(worlds):
        color = curses.color_pair(world.nivel)
        stdscr.addstr(i + 2, 0, f"[{i + 1}] {world.name} - {world.descricao} | ", curses.A_BOLD)
        stdscr.addstr(f"Nível {world.nivel}", color | curses.A_BOLD)

    stdscr.addstr(len(worlds) + 4, 0, "Pressione o número correspondente para escolher.", curses.A_BOLD)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(worlds):
            chosen_index = key - ord('1')
            world = worlds[chosen_index]
            draw_ascii_art(stdscr, world)
            return world


if __name__ == "__main__":
    curses.wrapper(choose_world)