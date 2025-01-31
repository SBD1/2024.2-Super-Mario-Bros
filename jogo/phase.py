from db import connect_to_db
import curses

class Fase:
    def __init__(self, id_phase, name):
        self.id_phase = id_phase
        self.name = name


def get_phase_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT DISTINCT idFase, nome FROM Fase"
            cursor.execute(query)
            phases = [Fase(id_phase=row[0], name=row[1]) for row in cursor.fetchall()]
        return phases
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def choose_phase(stdscr):
    """Exibe a tela para o jogador escolher a fase."""

    phases = get_phase_from_db()

    if not phases:
        stdscr.addstr(0, 0, "Nenhuma fase disponível no banco de dados!")
        stdscr.refresh()
        stdscr.getch()
        return None

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha em qual fase entrar:")

    for i, phase in enumerate(phases):
        stdscr.addstr(i + 1, 0, f"[{i + 1}] {phase.name}")

    stdscr.addstr(len(phases) + 2, 0, "Pressione o número correspondente para escolher.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(phases):
            chosen_index = key - ord('1')
            return phases[chosen_index]
    