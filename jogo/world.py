from db import connect_to_db
import curses

class Mundo:
    def __init__(self, id_mundo, name, descricao, nivel):
        self.id_mundo = id_mundo
        self.name = name
        self.descricao = descricao
        self.nivel = nivel


def get_world_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT DISTINCT idMundo, nome, descrição, nivel FROM Mundo"
            cursor.execute(query)
            worlds = [Mundo(id_mundo=row[0], name=row[1], descricao=row[2], nivel=row[3]) for row in cursor.fetchall()]
        return worlds
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def choose_world(stdscr):
    """Exibe a tela para o jogador escolher um mundo."""

    worlds = get_world_from_db()

    if not worlds:
        stdscr.addstr(0, 0, "Nenhum mundo disponível no banco de dados!", curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return None

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Verde → Fácil (1)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Amarelo → Médio (2)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Vermelho → Difícil (3)

    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha um mundo para entrar:", curses.A_BOLD)

    for i, world in enumerate(worlds):
        nivel_colors = {
            1: curses.color_pair(1), 
            2: curses.color_pair(2), 
            3: curses.color_pair(3) 
        }
        
        color = nivel_colors.get(world.nivel, curses.A_BOLD) 

        stdscr.addstr(i + 2, 0, f"[{i + 1}] {world.name} - {world.descricao} | ", curses.A_BOLD)
        stdscr.addstr(f"Nível {world.nivel}", color | curses.A_BOLD) 

    stdscr.addstr(len(worlds) + 4, 0, "Pressione o número correspondente para escolher.", curses.A_BOLD)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(worlds):
            chosen_index = key - ord('1')
            return worlds[chosen_index]
