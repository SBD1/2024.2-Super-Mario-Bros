import curses
import random
import time

# Configurações do jogo
SCENARIO_WIDTH = 20
OBSTACLE = "|"
GROUND_LEVEL = 1  # Linha do chão

player = None

# Função mockada para "conectar" ao banco de dados
def connect_to_db():
    print("Banco de dados mockado conectado!")


# Função principal do jogo
def init_game(stdscr):
    connect_to_db()
    time.sleep(1)

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Bem-vindo ao Super Mario Bros CLI")
    stdscr.refresh()
    stdscr.getch()

    character = choose_character(stdscr)

    phase = choose_phase(stdscr)
    local_phase = initial_local_by_phase(phase)
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"Você está na fase: {phase}")
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


# Mock da função que escolhe a fase
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
        

# Mock da função que escolhe o personagem
def choose_character(stdscr):
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

# Mock de localização inicial para cada fase
def initial_local_by_phase(phase):
    return 0  # Local inicial arbitrário

# Mock da exploração do local (não chama banco de dados)
def exploration_local(stdscr, local_phase, character):
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha uma direção para se mover (setas para mover):")
    stdscr.refresh()

    direction = stdscr.getch()
    new_local = local_phase
    encounter = None

    if direction == curses.KEY_UP:
        new_local, encounter = move_player(local_phase, "norte", character) 
    elif direction == curses.KEY_DOWN:
        new_local, encounter = move_player(local_phase, "sul", character) 
    elif direction == curses.KEY_LEFT:
        new_local, encounter = move_player(local_phase, "esquerda", character)
    elif direction == curses.KEY_RIGHT:
        new_local, encounter = move_player(local_phase, "direita", character)
    else:
        stdscr.addstr(3, 0, "Direção inválida")
    
    stdscr.refresh()
    stdscr.getch()

    return new_local, encounter

# Mock de movimento de jogador
def move_player(local_phase, direction, character):
    new_local = local_phase  # Mockando como se a posição não mudasse
    encounter = random.choice(["Combat", "loja", "blocos", "cano", "npc", None])  # Sorteando um encontro
    return new_local, encounter

# Mock de interação do jogador com o encontro
def player_turn(stdcsr, player, encounter):
    stdcsr.clear()

    if encounter == "Combat":
        stdcsr.addstr(0, 0, "Você encontrou inimigos! Se prepare para o combate.")
        mario_battle_turn(stdcsr, player)  # Iniciar o jogo com o personagem escolhido
    elif encounter == "loja":
        stdcsr.addstr(0, 0, "Você encontrou uma loja!")
        stdcsr.addstr(1, 0, "[1] Comprar")
        stdcsr.addstr(2, 0, "[2] Vender")
    elif encounter == "blocos":
        stdcsr.addstr(0, 0, "Você encontrou um bloco!")
        stdcsr.addstr(1, 0, "[1] Bater no bloco")
        stdcsr.addstr(2, 0, "[2] Ignorar bloco")
    elif encounter == "cano":
        stdcsr.addstr(0, 0, "Você encontrou um cano!")
        stdcsr.addstr(1, 0, "[1] Tentar entrar no cano")
        stdcsr.addstr(2, 0, "[2] Ignorar cano")
    elif encounter == "npc":
        stdcsr.addstr(0, 0, "Você encontrou um npc!")
        stdcsr.addstr(1, 0, "[1] Conversar com npc")
        stdcsr.addstr(2, 0, "[2] Ignorar npc")

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
    elif choice == "2":
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
    stdcsr.getch()

def generate_scenario(obstacles):
    """Gera o cenário atual."""
    scenario = [" " for _ in range(SCENARIO_WIDTH)]
    for pos in obstacles:
        if 0 <= pos < SCENARIO_WIDTH:
            scenario[pos] = OBSTACLE
    return "".join(scenario)

# Função mockada para simulação de batalha com Mario
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
        ground_line = scenario[:mario_position] + "M" + scenario[mario_position + 1:]
        air_line = " " * mario_position + "M" + " " * (SCENARIO_WIDTH - mario_position - 1)

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
