import curses
import random
import time

import psycopg2

# Configurações do jogo
SCENARIO_WIDTH = 20
OBSTACLE = "|"
GROUND_LEVEL = 1  # Linha do chão

player = None

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="supermario",
            user="root",
            password="123456",
            host="localhost",
            port="5432"
        )
        print("Conectado ao banco de dados!")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def generate_scenario(obstacles):
    """Gera o cenário atual."""
    scenario = [" " for _ in range(SCENARIO_WIDTH)]
    for pos in obstacles:
        if 0 <= pos < SCENARIO_WIDTH:
            scenario[pos] = OBSTACLE
    return "".join(scenario)


def init_game(stdscr):
    connect_to_db()
    time.sleep(1)
    
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Bem-vindo ao Super Mario Bros CLI")
    stdscr.refresh()
    stdscr.getch()

    character = choose_character(stdscr)  # Escolher o personagem
    
    phase = choose_phase(stdscr)  # Escolher a fase
    local_phase = initial_local_by_phase(phase) # Fazer consulta sql para retornar qual é o local iniciar da fase
    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {phase.name}")
    stdscr.refresh()
    stdscr.getch()

    while character:
        local_phase, encounter = exploration_local(stdscr, local_phase, character)
        if encounter:
            player_turn(stdscr, player, encounter)

        if not character:        
            stdscr.clear()
            stdscr.addstr(0, 0, f"{character} foi derrotado")
            stdscr.refresh()
            stdscr.getch()


# Inicia o jogo chamando `init_game`
curses.wrapper(init_game)