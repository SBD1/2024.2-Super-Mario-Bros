from character import choose_character
from battle import turno_batalha, entrar_fase
from phase import choose_phase
from local import initial_local_by_phase, exploration_local, get_encounter_by_local
from world import choose_world
from loja import get_loja_with_items, comprar_item, vender_item, get_lojaId_by_world
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

    character = choose_character(stdscr) 
    
    world = choose_world(stdscr)

    selected_phase = choose_phase(stdscr, world.id_mundo) 

    if visit_shop(stdscr):
        open_shop(stdscr, character, world)

    
    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {selected_phase.name}")
    stdscr.refresh()
    stdscr.getch()

    while character.vida != 0:
        resultado = entrar_fase(stdscr, character, selected_phase)
        if resultado == "venceu":
            print("passar de fase")
        else:
            stdscr.clear()
            stdscr.addstr(0, 0, "Você perdeu, deseja tentar novamente? (S/N)")
            stdscr.refresh()
            key = stdscr.getch()
            if key in (ord('n'), ord('N')):
                break

    if visit_shop(stdscr):
        open_shop(stdscr, character, world)
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"{character.nome} foi derrotado")
    stdscr.refresh()
    stdscr.getch()

def visit_shop(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Deseja visitar a loja? (S/N)")
    stdscr.refresh()
    key = stdscr.getch()
    return key in (ord('s'), ord('S'))

def open_shop(stdscr, player, world):
    loja_id = get_lojaId_by_world(world.id_mundo)
    stdscr.addstr(row, 0, "Você encontrou uma loja!")
    row += 1
    stdscr.addstr(row, 0, "[1] Comprar")
    row += 1
    stdscr.addstr(row, 0, "[2] Vender")

    choice = stdscr.getkey()

    if choice == "1":
        loja = get_loja_with_items(loja_id)
        comprar_item(stdscr, player, loja)
    elif choice == "2":
        loja = get_loja_with_items()
        vender_item(stdscr, player.id, loja)




# Inicia o jogo chamando `init_game`
curses.wrapper(init_game)