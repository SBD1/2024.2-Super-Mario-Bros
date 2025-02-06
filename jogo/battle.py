import curses
import random
import time


class Instancia:
    def __init__(self, id_personagem, vidaAtual, moedaAtual, pontosAtual):
        self.id = id_personagem
        self.vida = vidaAtual
        self.moedas = moedaAtual
        self.pontos = pontosAtual

SCENARIO_WIDTH = 20
OBSTACLE = "|"
ENEMY = "E"
GROUND_LEVEL = 1  # Linha do chão
ENEMY_MOVE_DELAY = 10  # A cada quantos ciclos os inimigos se movem

def generate_scenario(obstacles, enemies):
    scenario = [" "] * SCENARIO_WIDTH
    for pos in obstacles:
        scenario[pos] = OBSTACLE
    for pos in enemies:
        scenario[pos] = ENEMY
    return "".join(scenario)

def mario_battle_turn(stdscr, character):
    curses.curs_set(0)  # Ocultar o cursor
    stdscr.nodelay(1)   # Não bloquear para entrada
    stdscr.timeout(200) # Atualizar a tela a cada 200ms
    
    score = 0
    lives = 3
    mario_position = 1
    obstacles = [random.randint(10, SCENARIO_WIDTH - 1)]
    enemies = [random.randint(5, SCENARIO_WIDTH - 1)]
    mario_y = GROUND_LEVEL  # Altura atual do Mario
    jumping = False         # Indica se o Mario está pulando
    jump_phase = 0          # Fases do pulo (subindo/descendo)
    enemy_move_timer = 0    # Timer para movimentar os inimigos
    difficulty = 1          # Nível de dificuldade (quanto mais alto, mais obstáculos)

    while lives > 0:
        stdscr.clear()
        
        # Gera o cenário
        scenario = generate_scenario(obstacles, enemies)
        ground_line = scenario[:mario_position] + character + scenario[mario_position + 1:]
        air_line = " " * mario_position + character + " " * (SCENARIO_WIDTH - mario_position - 1)
        
        # Mostra o cenário com Mario na posição correta
        if mario_y == GROUND_LEVEL:
            stdscr.addstr(0, 0, " " * SCENARIO_WIDTH)  # Linha de cima vazia
            stdscr.addstr(1, 0, ground_line)          # Mario no chão
        else:
            stdscr.addstr(0, 0, air_line)             # Mario no ar
            stdscr.addstr(1, 0, scenario)            # Obstáculos e inimigos no chão

        stdscr.addstr(2, 0, f"Score: {score}  |  Lives: {lives}  |  Difficulty: {difficulty}")
        
        # Atualiza obstáculos e inimigos
        obstacles = [pos - 1 for pos in obstacles if pos - 1 > 0]
        enemies = [pos + 1 for pos in enemies if pos + 1 < SCENARIO_WIDTH]

        # Gerar novos obstáculos e inimigos com base no nível de dificuldade
        if random.random() < 0.3 + 0.1 * difficulty:
            obstacles.append(SCENARIO_WIDTH - 1)
        if random.random() < 0.2 + 0.1 * difficulty:
            enemies.append(SCENARIO_WIDTH - 1)
        
        # Lógica para os inimigos se moverem
        enemy_move_timer += 1
        if enemy_move_timer >= ENEMY_MOVE_DELAY - difficulty:  # Inimigos se movem a cada vez mais rápido
            enemies = [pos + 1 if random.choice([True, False]) else pos - 1 for pos in enemies]
            enemy_move_timer = 0

        # Verifica colisão ou pulo sobre o obstáculo
        if mario_y == GROUND_LEVEL:
            if mario_position in obstacles:
                if jumping:  # Pular sobre o obstáculo
                    obstacles.remove(mario_position)  # Remove o obstáculo se Mario pulou
                    score += 5  # Pontos extras por pular sobre o obstáculo
                    stdscr.addstr(3, 0, "Você pulou sobre o obstáculo!")
                else:  # Colidiu com o obstáculo
                    lives -= 1
                    stdscr.addstr(3, 0, "Você bateu no obstáculo!")
            elif mario_position in enemies:  # Colisão com inimigo
                if jumping:  # Mario pode pular no inimigo
                    enemies.remove(mario_position)  # Remove o inimigo se Mario pulou
                    score += 10  # Pontos por derrotar inimigo
                    stdscr.addstr(3, 0, "Você pulou no inimigo e derrotou-o!")
                else:  # Mario bateu no inimigo
                    lives -= 1
                    stdscr.addstr(3, 0, "Você bateu no inimigo!")
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
        elif key == ord('a'):  # 'a' para mover para a esquerda
            if mario_position > 0:
                mario_position -= 1
        elif key == ord('d'):  # 'd' para mover para a direita
            if mario_position < SCENARIO_WIDTH - 1:
                mario_position += 1

        # Atualiza o nível de dificuldade à medida que o jogo avança
        if score > 50:
            difficulty = 2
        if score > 100:
            difficulty = 3

        # Atualiza score
        score += 1

        stdscr.refresh()
        time.sleep(0.1)

    # Fim de jogo
    stdscr.clear()
    stdscr.addstr(0, 0, f"Fim do Jogo! Sua pontuação final foi: {score}")
    stdscr.refresh()
    time.sleep(2)
