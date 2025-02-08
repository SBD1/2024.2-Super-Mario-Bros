import curses 
import random
import time

# Definição dos pontos e siglas dos inimigos
ENEMY_POINTS = {
    "Goomba": 10,
    "Koopa Troopa": 15,
    "Boo": 20,
    "Thwomp": 30,
    "Dry Bones": 25,
    "Chain Chomp": 40,
    "Boohemoth": 50
}

ENEMY_ABBREVIATIONS = {
    "Goomba": "G",
    "Koopa Troopa": "K",
    "Boo": "B",
    "Thwomp": "T",
    "Dry Bones": "D",
    "Chain Chomp": "C",
    "Boohemoth": "H"
}

ITEMS = {"F": "Fireball", "I": "Ice Flower", "B": "Boomerang", "S": "Starman"}

SCENARIO_WIDTH = 40
OBSTACLE = "|"
GROUND_LEVEL = 1  

class Instancia:
    def __init__(self, id_personagem, vidaAtual, moedaAtual, pontosAtual):
        self.id = id_personagem
        self.vida = vidaAtual
        self.moedas = moedaAtual
        self.pontos = pontosAtual

def generate_scenario(obstacles, enemies, items):
    scenario = [" "] * SCENARIO_WIDTH

    for pos in obstacles:
        if scenario[pos] == " ":
            scenario[pos] = OBSTACLE

    for pos, enemy_type in enemies.items():
        if scenario[pos] == " ":
            scenario[pos] = ENEMY_ABBREVIATIONS.get(enemy_type, "?")

    for pos, item in items.items():
        if scenario[pos] == " ":
            scenario[pos] = item

    return "".join(scenario)


def mario_battle_turn(stdscr, character):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(200)

    score = 0
    lives = 3
    mario_position = 1
    obstacles = [random.randint(10, SCENARIO_WIDTH - 1)]
    enemies = {random.randint(5, SCENARIO_WIDTH - 1): random.choice(list(ENEMY_POINTS.keys()))}
    items = {random.randint(5, SCENARIO_WIDTH - 1): random.choice(list(ITEMS.keys()))}
    mario_y = GROUND_LEVEL  
    jumping = False  
    jump_phase = 0  
    collected_items = []  
    invincible_timer = 0  

    while lives > 0:
        stdscr.clear()
        
        if invincible_timer > 0:
            invincible_timer -= 1

        scenario = generate_scenario(obstacles, enemies, items)
        ground_line = scenario[:mario_position] + "M" + scenario[mario_position + 1:]
        air_line = " " * mario_position + "M" + " " * (SCENARIO_WIDTH - mario_position - 1)

        if mario_y == GROUND_LEVEL:
            stdscr.addstr(0, 0, " " * SCENARIO_WIDTH)
            stdscr.addstr(1, 0, ground_line)
        else:
            stdscr.addstr(0, 0, air_line)
            stdscr.addstr(1, 0, scenario)

        stdscr.addstr(0, 0, f"Score: {score}  |  Lives: {lives}  |  Items: {', '.join([ITEMS[i] for i in collected_items])}  |  Invincible: {invincible_timer}")
        
        obstacles = [pos - 1 for pos in obstacles if pos - 1 > 0]
        enemies = {pos - 1: enemy for pos, enemy in enemies.items() if pos - 1 > 0}
        items = {pos - 1: item for pos, item in items.items() if pos - 1 > 0}

        if random.random() < 0.1:
            obstacles.append(SCENARIO_WIDTH - 1)
        if random.random() < 0.05:
            enemy_type = random.choice(list(ENEMY_POINTS.keys()))
            enemies[SCENARIO_WIDTH - 1] = enemy_type
        if random.random() < 0.05:
            items[random.randint(5, SCENARIO_WIDTH - 1)] = random.choice(list(ITEMS.keys()))

        if mario_y == GROUND_LEVEL:
            if mario_position in obstacles:
                if jumping:
                    obstacles.remove(mario_position)
                    score += 5
                    stdscr.addstr(3, 0, "Você pulou sobre o obstáculo!")
                else:
                    lives -= 1
                    stdscr.addstr(3, 0, "Você bateu no obstáculo!")
            elif mario_position in enemies:
                enemy_type = enemies[mario_position]
                if enemy_type == "Boo" and "S" in collected_items:
                    del enemies[mario_position]
                    score += ENEMY_POINTS[enemy_type]
                    stdscr.addstr(3, 0, f"Você derrotou o Boo com a Estrela!")
                elif enemy_type == "Boo" and "I" in collected_items:
                    del enemies[mario_position]
                    score += ENEMY_POINTS[enemy_type]
                    stdscr.addstr(3, 0, f"Você congelou o Boo!")
                elif enemy_type != "Boo":
                    if "S" in collected_items or jumping:
                        del enemies[mario_position]
                        score += ENEMY_POINTS[enemy_type]
                        stdscr.addstr(3, 0, f"Você derrotou {enemy_type}!")
                    else:
                        lives -= 1
                        stdscr.addstr(3, 0, f"Você bateu em {enemy_type}!")

            elif mario_position in items:
                item = items[mario_position]
                if item not in collected_items:
                    collected_items.append(item)
                    stdscr.addstr(3, 0, f"Você pegou {ITEMS[item]}!")
                    if item == "S":
                        invincible_timer = 20
                del items[mario_position]

        if jumping:
            if jump_phase < 2:
                mario_y = 0
                jump_phase += 1
            else:
                mario_y = GROUND_LEVEL
                jumping = False
                jump_phase = 0

        key = stdscr.getch()
        if key == ord(' '):
            if mario_y == GROUND_LEVEL:
                jumping = True
        elif key == ord('q'):
            break
        elif key == ord('a'):
            if mario_position > 0:
                mario_position -= 1
        elif key == ord('d'):
            if mario_position < SCENARIO_WIDTH - 1:
                mario_position += 1
        elif key == ord('f') and "F" in collected_items:
            if enemies:
                enemy_pos = list(enemies.keys())[0]
                enemy_type = enemies[enemy_pos]
                score += ENEMY_POINTS[enemy_type]
                del enemies[enemy_pos]
                stdscr.addstr(3, 0, f"Fireball derrotou {enemy_type}! Ganhou {ENEMY_POINTS[enemy_type]} pontos!")

        score += 1

        stdscr.refresh()
        time.sleep(0.1)

    stdscr.clear()
    stdscr.addstr(0, 0, f"Fim do Jogo! Sua pontuação final foi: {score}")
    stdscr.refresh()
    time.sleep(2)
