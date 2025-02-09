from character import choose_character, player_turn
from phase import choose_phase
from local import initial_local_by_phase, exploration_local, get_encounter_by_local
from world import choose_world
from db import connect_to_db

import curses
import random
import time

import psycopg2

# Configurações do jogo
SCENARIO_WIDTH = 20
OBSTACLE = "|"
GROUND_LEVEL = 1  # Linha do chão

player = None

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
    stdscr.addstr(0, 0, "Bem-vindo ao Super Mario Bros CLI\n")
    stdscr.refresh()
    stdscr.getch()

    character = choose_character(stdscr)  # Escolher o personagem
    
    world = choose_world(stdscr) # Escolher o mundo
    phase = choose_phase(stdscr, world.id_mundo)  # Escolher a fase
    local_phase = initial_local_by_phase(phase) # Fazer consulta sql para retornar qual é o local iniciar da fase
    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {phase.name}")
    stdscr.refresh()
    stdscr.getch()

    while character.vida != 0:
        encounter = get_encounter_by_local(local_phase)
        if encounter:
            player_turn(stdscr, character, encounter)

        local_phase, encounter = exploration_local(stdscr, phase.id_phase, local_phase, character.id)
        if encounter:
            player_turn(stdscr, character, encounter)

    stdscr.clear()
    stdscr.addstr(0, 0, f"{character} foi derrotado")
    stdscr.refresh()
    stdscr.getch()


# Inicia o jogo chamando `init_game`
curses.wrapper(init_game)