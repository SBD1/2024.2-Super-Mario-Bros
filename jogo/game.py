from character import choose_character
from battle import turno_batalha
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
    
    # Escolher o mundo
    world = choose_world(stdscr)  # Escolher o mundo

    # Escolher a fase
    selected_phase = choose_phase(stdscr, world.id_mundo)  # Escolher a fase

    # Agora, use a variável selected_phase
    if selected_phase:
        # Passa a fase escolhida para a função que define o local inicial da fase
        local_phase = initial_local_by_phase(selected_phase)
    else:
        # Caso não tenha escolhido uma fase válida, pode adicionar um tratamento de erro
        stdscr.addstr(0, 0, "Nenhuma fase selecionada!")
        stdscr.refresh()
        stdscr.getch()
        return None


    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {selected_phase.name}")
    stdscr.refresh()
    stdscr.getch()

    while character.vida != 0:
        encounter = get_encounter_by_local(local_phase)
        if encounter:
            turno_batalha(stdscr, character, encounter, mapa, items)  # Chama a função de batalha

        local_phase, encounter = exploration_local(stdscr, selected_phase.id_phase, local_phase, character.id)
        if encounter:
            turno_batalha(stdscr, character, encounter, mapa, items)  # Chama a função de batalha

        if local_phase.is_final_local:
            print("Último local da fase")

    stdscr.clear()
    stdscr.addstr(0, 0, f"{character} foi derrotado")
    stdscr.refresh()
    stdscr.getch()



# Inicia o jogo chamando `init_game`
curses.wrapper(init_game)