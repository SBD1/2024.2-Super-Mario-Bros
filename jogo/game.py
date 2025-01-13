import curses
import random
import time

import psycopg2

# Configurações do jogo
SCENARIO_WIDTH = 20
OBSTACLE = "|"
GROUND_LEVEL = 1  # Linha do chão


class Fase:
    def __init__(self, id_phase, name):
        self.id_phase = id_phase
        self.name = name

class Local:
    def __init__(self, id_local, name, description):
        self.id_local = id_local
        self.name = name
        self.description = description


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
        stdscr.addstr(i + 1, 0, f"[{i}] {phase.name}")

    stdscr.addstr(len(phases) + 2, 0, "Pressione o número correspondente para escolher.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(phases):
            chosen_index = key - ord('1')
            return phases[chosen_index]
        

def initial_local_by_phase(id_phase):
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT nome, descricao FROM Local WHERE idFase = %s"
            cursor.execute(query, (id_phase,))
            locais = cursor.fetchall()

        if not locais:
            return f"Nemhum local encontrado para a fase com idFase = {id_phase}."
        
        local_aleatorio = random.choice(locais)
        nome_local, descricao_local = local_aleatorio
        local = Local(name=nome_local, description=descricao_local)

        return local
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def get_characters_from_db():
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT tipo FROM Jogador"
            cursor.execute(query)
            characters = [row[0] for row in cursor.fetchall()]
        return characters
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def choose_character(stdscr):
    """Exibe a tela para o jogador escolher o personagem."""

    characters = get_characters_from_db()

    if not characters:
        stdscr.addstr(0, 0, "Nenhum personagem disponível no banco de dados!")
        stdscr.refresh()
        stdscr.getch()
        return None

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha seu personagem:")

    for i, character in enumerate(characters):
        stdscr.addstr(i + 1, 0, f"[{i}] {character}")

    stdscr.addstr(len(characters) + 2, 0, "Pressione o número correspondente para escolher.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(characters):
            chosen_index = key - ord('1')
            return characters[chosen_index]

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

def move_player(local_phase, direction, character):
    if direction == "norte":
        new_local = get_local_phase_by_direction()
        encounter = get_encount_by_direction()
    if direction == "sul":
        new_local = get_local_phase_by_direction()        
        encounter = get_encount_by_direction()
    
    # Atualizar em sql a nova posição do jogador 

    return new_local, encounter

def player_turn(stdcsr, player, encounter):
    while True:
        stdcsr.clear()
        
        if encounter == "Combat":
            stdcsr.addstr(0, 0, "Você encontrou inimigos! Se prepare para o combate.")
            mario_battle_turn(stdscr, player)  # Iniciar o jogo com o personagem escolhido
        elif encounter == "loja":
            stdcsr.addstr(0, 0, "Você encontrou uma loja!")
            stdcsr.addstr(0, 1, "[1] Comprar")
            stdcsr.addstr(0, 2, "[2] Vender")
        elif encounter == "blocos":
            stdcsr.addstr(0, 0, "Você encontrou uma blocos!")
            stdcsr.addstr(0, 1, "[1] Bater no bloco")
            stdcsr.addstr(0, 2, "[2] Ignora bloco")
        elif encounter == "cano":
            stdcsr.addstr(0, 0, "Você encontrou uma cano!")
            stdcsr.addstr(0, 1, "[1] Tentar entrar no cano")
            stdcsr.addstr(0, 2, "[2] Ignorar cano")
        elif encounter == "npc":
            stdcsr.addstr(0, 0, "Você encontrou um npc!")
            stdcsr.addstr(0, 1, "[1] Conversar com npc")
            stdcsr.addstr(0, 2, "[2] Ignorar npc")

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
        elif choice == "1":
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