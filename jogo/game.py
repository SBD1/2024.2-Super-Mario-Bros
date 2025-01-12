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
    local_phase = initial_local_by_phase(phase)
    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {phase}")
    stdscr.refresh()
    stdscr.getch()

    while character:
        encounter = exploration_local(stdscr, local_phase, character)
        if encounter:
            player_turn(stdscr, player, encounter)

        if not character:        
            stdscr.clear()
            stdscr.addstr(0, 0, f"{character} foi derrotado")
            stdscr.refresh()
            stdscr.getch()


def choose_phase(stdscr):
    """Exibe a tela para o jogador escolher a fase."""
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha a fase:")
    stdscr.addstr(1, 0, "[1] Floresta Tal Tal")
    stdscr.addstr(2, 0, "[2] Deserto")
    stdscr.addstr(3, 0, "[3] Montanha")
    stdscr.addstr(5, 0, "Pressione o número correspondente à fase.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            return '1'
        elif key == ord('2'):
            return '2'
        elif key == ord('3'):
            return '3'


def choose_character(stdscr):
    """Exibe a tela para o jogador escolher o personagem."""
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha seu personagem:")
    stdscr.addstr(1, 0, "[M] Mario")
    stdscr.addstr(2, 0, "[L] Luigi")
    stdscr.addstr(4, 0, "Pressione a tecla correspondente (M ou L) para começar.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('m') or key == ord('M'):
            return "M"
        elif key == ord('l') or key == ord('L'):
            return "L"

def exploration_local(stdscr, local_phase, character):
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha uma direção para se mover (sul, norte):")
    stdscr.refresh()

    direction = stdscr.getkey()
    if direction in ["up", "down"]:
        encounter = move_player(local_phase, direction, character) # vai moter o jogador de local e retorna o que foi encontrado

    else:
        stdscr.addstr(3, 0, "Direção inválida")
        encounter = None
    stdscr.refresh()
    stdscr.getch()

    return encounter

def player_turn(stdcsr, player, encounter):
    while True:
        stdcsr.clear()
        
        if encounter == "Combat":
            stdcsr.addstr(0, 0, "Você encontrou inimigos! Se prepare para o combate.")
            mario_battle_turn(stdscr, player)  # Iniciar o jogo com o personagem escolhido
        elif encounter == "shop":
            stdcsr.addstr(0, 0, "Você encontrou uma loja!")
            stdcsr.addstr(0, 1, "[1]")
            stdcsr.addstr(0, 2, "[2]")
        elif encounter == "blocos":
            stdcsr.addstr(0, 0, "Você encontrou uma blocos!")
            stdcsr.addstr(0, 1, "[1]")
            stdcsr.addstr(0, 2, "[2]")
        elif encounter == "cano":
            stdcsr.addstr(0, 0, "Você encontrou uma cano!")
            stdcsr.addstr(0, 1, "[1]")
            stdcsr.addstr(0, 2, "[2]")

        stdcsr.refresh()
        choice = stdcsr.getkey()

        if choice == "1":
            print("resultados da escolha 1")
        elif choice == "1":
            print("resultados da escolha 1")
        else:
            stdcsr.addstr(4, 0, "Escolha inválida. Tente novamente.")

        stdcsr.refresh()
        stdcsr.gettch()


def mario_battle_turn(stdscr, character):
    curses.curs_set(0)  # Ocultar o cursor
    stdscr.nodelay(1)   # Não bloquear para entrada
    stdscr.timeout(200) # Atualizar a tela a cada 200ms
    
    score = 0
    lives = 3
    mario_position = 1
    obstacles = [random.randint(10, SCENARIO_WIDTH - 1)]
    mario_y = GROUND_LEVEL  # Altura atual do Mario
    jumping = False         # Indica se o Mario está pulando
    jump_phase = 0          # Fases do pulo (subindo/descendo)

    while lives > 0:
        stdscr.clear()
        
        # Gera o cenário
        scenario = generate_scenario(obstacles)
        ground_line = scenario[:mario_position] + character + scenario[mario_position + 1:]
        air_line = " " * mario_position + character + " " * (SCENARIO_WIDTH - mario_position - 1)
        
        # Mostra o cenário com Mario na posição correta
        if mario_y == GROUND_LEVEL:
            stdscr.addstr(0, 0, " " * SCENARIO_WIDTH)  # Linha de cima vazia
            stdscr.addstr(1, 0, ground_line)          # Mario no chão
        else:
            stdscr.addstr(0, 0, air_line)             # Mario no ar
            stdscr.addstr(1, 0, scenario)            # Obstáculos no chão

        stdscr.addstr(2, 0, f"Score: {score}  |  Lives: {lives}")
        
        # Atualiza obstáculos
        obstacles = [pos - 1 for pos in obstacles if pos - 1 > 0]
        if random.random() < 0.3:
            obstacles.append(SCENARIO_WIDTH - 1)

        # Detecta colisão
        if mario_y == GROUND_LEVEL and mario_position in obstacles:
            lives -= 1
            stdscr.addstr(3, 0, "Você bateu no obstáculo!")
        else:
            stdscr.addstr(3, 0, "Correndo...")

        # Pulo
        if jumping:
            if jump_phase < 2:  # Subindo
                mario_y = 0
                jump_phase += 1
            else:  # Descendo
                mario_y = GROUND_LEVEL
                jumping = False
                jump_phase = 0

        # Entrada do jogador
        key = stdscr.getch()
        if key == ord(' '):  # Barra de espaço para pular
            if mario_y == GROUND_LEVEL:  # Só pode pular se estiver no chão
                jumping = True
        elif key == ord('q'):  # 'q' para sair
            break

        # Atualiza score
        score += 1

        stdscr.refresh()
        time.sleep(0.1)

    # Fim de jogo
    stdscr.clear()
    stdscr.addstr(0, 0, f"Game Over! Sua pontuação final foi: {score}")
    stdscr.refresh()
    time.sleep(2)


# Inicia o jogo chamando `init_game`
curses.wrapper(init_game)