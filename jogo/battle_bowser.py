import curses
import random
import pyfiglet  # Importando o pyfiglet
import pygame
import os

# Definindo o personagem Mario
class Mario:
    def __init__(self, mapa):
        self.vida = 100
        self.pontos = 0
        self.posicao = [1, 1]  # Posição inicial do Mario na matriz (1, 1)
        self.checkpoint = self.gerar_posicao_aleatoria(mapa)  # Gerar o checkpoint aleatório
        self.salvou_checkpoint = False  # Indica se Mario já salvou o checkpoint

    def gerar_posicao_aleatoria(self, mapa):
        while True:
            x = random.randint(0, len(mapa) - 1)
            y = random.randint(0, len(mapa[0]) - 1)
            if mapa[x][y] != 'M':  # Garantir que a posição não seja ocupada pelo Mario
                return [x, y]

    def mover(self, direcao, mapa):
        nova_posicao = self.posicao[:]
        
        if direcao == "UP":
            nova_posicao[0] -= 1
        elif direcao == "DOWN":
            nova_posicao[0] += 1
        elif direcao == "LEFT":
            nova_posicao[1] -= 1
        elif direcao == "RIGHT":
            nova_posicao[1] += 1

        # Verifica se a nova posição está dentro dos limites da matriz
        if 0 <= nova_posicao[0] < len(mapa) and 0 <= nova_posicao[1] < len(mapa[0]):
            self.posicao = nova_posicao
            # print(f"Mario se moveu para {self.posicao}")
            
            # Verifica se Mario passou pela posição do checkpoint
            if self.posicao == self.checkpoint and not self.salvou_checkpoint:
                self.salvou_checkpoint = True
                print("Checkpoint salvo!")
                curses.napms(1000)  # Espera 2 segundos para dar tempo de ver a mensagem
        else:
            print("Movimento inválido!")

    def atacar(self, item, inimigo):
        dano = 0
        if item == 'Fireball':
            dano = 30
        elif item == 'Boomerang':
            dano = 20
        
        if dano > 0:
            inimigo.perder_vida(dano)
            return dano
        return 0

    def pular(self, inimigo):
        print("Mario pula para atacar o inimigo!")
        
        # O dano do pulo é menor e causa dano instantâneo no Goomba
        dano_pulo = 10
        if inimigo.nome == "Goomba":
            inimigo.perder_vida(inimigo.vida)  # Goomba morre instantaneamente
            print(f"Goomba foi derrotado instantaneamente!")
        else:
            inimigo.perder_vida(dano_pulo)
            print(f"{inimigo.nome} sofreu {dano_pulo} de dano pelo pulo!")

    def desviar(self):
        print("Mario desvia do ataque do inimigo!")

# Função para exibir o mapa
def exibir_mapa(stdscr, mario, mapa):
    stdscr.clear()  # Limpa a tela antes de desenhar o mapa
    
    # Obtendo as dimensões da janela do terminal
    altura, largura = stdscr.getmaxyx()

    # Usando pyfiglet para criar uma arte ASCII do título "FASE 1"
    titulo_ascii = pyfiglet.figlet_format("FASE BOWSER", font="slant")  # Usando a fonte "slant" como exemplo
    
    # Centralizando o título ASCII no topo da tela
    titulo_x = (largura // 2) - (len(titulo_ascii.split("\n")[0]) // 2)
    
    # Exibindo o título bonito no topo da tela
    for i, linha in enumerate(titulo_ascii.split("\n")):
        stdscr.addstr(i, titulo_x, linha)
    
    # Calculando o início para a matriz (centralizada na tela)
    mapa_inicio_x = (largura // 2) - (len(mapa[0]) * 2 // 2)  # Para centralizar horizontalmente a matriz
    mapa_inicio_y = (altura // 2) - (len(mapa) // 2)  # Para centralizar verticalmente a matriz
    
    # Exibindo a matriz do mapa
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if [i, j] == mario.posicao:
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, "M")  # Exibe 'M' para Mario
            elif mapa[i][j] == 'X':  # Exibe 'X' para indicar a posição da batalha (após a derrota do inimigo)
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, "X")
            elif mapa[i][j] == 'I':  # Exibe 'I' para indicar o inimigo, quando Mario perde
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, "I")
            elif mapa[i][j] == 'C':  # Exibe 'C' para indicar o cogumelo
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, "C")
            elif mapa[i][j] == 'B':  # Exibe 'B' para indicar o Bowser
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, "B")
            else:
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, ".")  # Exibe '.' para as outras células
    
    stdscr.refresh()

# Função para rodar um turno de batalha
class Inimigo:
    def __init__(self, nome, vida, dano, pontos, mapa=None):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.pontos = pontos
        self.posicao = self.gerar_posicao_aleatoria(mapa)  # Posição aleatória para o inimigo
        self.derrotado = False  # Indica se o inimigo foi derrotado

    def gerar_posicao_aleatoria(self, mapa):
        if mapa is None:  # Se o mapa não foi fornecido, retorna uma posição padrão
            return [0, 0]
        
        while True:
            x = random.randint(0, len(mapa) - 1)
            y = random.randint(0, len(mapa[0]) - 1)
            if mapa[x][y] != 'M' and mapa[x][y] != 'C':  # Garantir que a posição não seja ocupada por Mario ou pelo checkpoint
                return [x, y]

    def atacar(self):
        return self.dano

    def perder_vida(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.derrotado = True  # Marca como derrotado quando a vida chegar a zero

# Classe Bowser, um inimigo especial
class Bowser(Inimigo):
    def __init__(self):
        super().__init__("Bowser", 150, 25, 200, mapa=None)  # Bowser tem mais vida e causa mais dano
        self.defesa_ativa = False  # Indica se a defesa está ativa

    def atacar(self):
        # Bowser tem uma chance de causar dano crítico
        if random.random() < 0.3:  # 30% de chance de dano crítico
            return self.dano * 2
        return self.dano

    def ataque_especial(self):
        # Bowser pode cuspir fogo ou atacar com a cauda
        if random.random() < 0.5:
            return self.dano * 1.5  # Ataque de fogo
        else:
            return self.dano * 2  # Ataque de cauda

    def defender(self):
        # Bowser se defende, reduzindo o dano recebido
        self.defesa_ativa = True
        return "Bowser se defendeu, reduzindo o dano recebido!"

# Função para criar a matriz de batalha contra o Bowser
def criar_matriz_batalha_bowser():
    # Cria uma matriz 12x12 para a batalha contra o Bowser
    matriz_batalha = [['.' for _ in range(12)] for _ in range(12)]
    
    # Posiciona o Bowser no centro da matriz
    matriz_batalha[5][5] = 'B'  # Bowser
    
    # Posiciona os fogos em posições aleatórias
    for _ in range(5):  # 5 fogos
        x, y = random.randint(0, 11), random.randint(0, 11)
        while matriz_batalha[x][y] != '.':
            x, y = random.randint(0, 11), random.randint(0, 11)
        matriz_batalha[x][y] = 'F'  # Fogo
    
    # Posiciona os itens que Mario pode acertar
    for _ in range(3):  # 3 itens
        x, y = random.randint(0, 11), random.randint(0, 11)
        while matriz_batalha[x][y] != '.':
            x, y = random.randint(0, 11), random.randint(0, 11)
        matriz_batalha[x][y] = 'I'  # Item
    
    return matriz_batalha

# Função para mover os fogos na matriz
def mover_fogos(matriz_batalha):
    for i in range(len(matriz_batalha)):
        for j in range(len(matriz_batalha[i])):
            if matriz_batalha[i][j] == 'F':
                # Move o fogo em uma direção aleatória
                direcao = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
                nova_posicao = [i, j]
                if direcao == 'UP':
                    nova_posicao[0] -= 1
                elif direcao == 'DOWN':
                    nova_posicao[0] += 1
                elif direcao == 'LEFT':
                    nova_posicao[1] -= 1
                elif direcao == 'RIGHT':
                    nova_posicao[1] += 1

                # Verifica se a nova posição é válida
                if 0 <= nova_posicao[0] < 12 and 0 <= nova_posicao[1] < 12:
                    if matriz_batalha[nova_posicao[0]][nova_posicao[1]] == '.':
                        matriz_batalha[i][j] = '.'
                        matriz_batalha[nova_posicao[0]][nova_posicao[1]] = 'F'

def turno_batalha(stdscr, mario, inimigo, mapa, music_channel):
    # Verifica se o inimigo foi derrotado antes de iniciar a batalha
    if inimigo.derrotado:
        return True  # Retorna imediatamente, não continua a batalha

    stdscr.clear()
    stdscr.addstr(0, 0, f"Início do turno de Mario! Vida de Mario: {mario.vida}, Pontos: {mario.pontos}")
    stdscr.addstr(1, 0, f"Inimigo: {inimigo.nome}, Vida: {inimigo.vida}")
    stdscr.addstr(3, 0, "Escolha sua ação: [F] Usar Flor de Fogo, [B] Usar Boomerang, [Q] Pular, [E] Desviar")
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == ord('f') or key == ord('F'):  # Usar a Flor de Fogo
            item = 'Fireball'
            dano = mario.atacar(item, inimigo)
            stdscr.addstr(5, 0, f"\nMario ataca com Flor de Fogo! Causa {dano} de dano no {inimigo.nome}.")
        elif key == ord('b') or key == ord('B'):  # Usar o Boomerang
            item = 'Boomerang'
            dano = mario.atacar(item, inimigo)
            stdscr.addstr(5, 0, f"\nMario ataca com Boomerang! Causa {dano} de dano no {inimigo.nome}.")
        elif key == ord('q') or key == ord('Q'):  # Pular
            dano_pulo = 10
            if inimigo.nome == "Goomba":
                inimigo.perder_vida(inimigo.vida)  # Goomba morre instantaneamente
                stdscr.addstr(5, 0, f"Goomba foi derrotado instantaneamente!")
                stdscr.refresh()
                curses.napms(2000)
                mario.pontos += inimigo.pontos  # Adiciona os pontos do Goomba
            elif inimigo.nome == "Koopa Troopa":
                inimigo.perder_vida(dano_pulo)  # Koopa Troopa leva o dano de 10
                stdscr.addstr(5, 0, f"{inimigo.nome} sofreu {dano_pulo} de dano pelo pulo!")
                if inimigo.vida <= 0:
                    mario.pontos += inimigo.pontos  # Adiciona os pontos do Koopa Troopa
            break

        elif key == ord('e') or key == ord('E'):  # Desviar
            mario.desviar(mapa)
            break

        # Mostrar a vida atual do inimigo e Mario após o ataque
        stdscr.clear()
        stdscr.addstr(0, 0, f"Início do turno de Mario! Vida de Mario: {mario.vida}, Pontos: {mario.pontos}")
        stdscr.addstr(1, 0, f"Inimigo: {inimigo.nome}, Vida: {inimigo.vida}")
        stdscr.addstr(3, 0, "Escolha sua ação: [F] Usar Flor de Fogo, [B] Usar Boomerang, [Q] Pular, [E] Desviar")
        stdscr.addstr(6, 0, f"Vida atual de {inimigo.nome}: {inimigo.vida}")
        stdscr.addstr(7, 0, f"Vida de Mario: {mario.vida}")
        stdscr.refresh()

        # Verificando se o inimigo foi derrotado
        if inimigo.vida <= 0:
            mario.pontos += inimigo.pontos
            stdscr.addstr(8, 0, f"{inimigo.nome} foi derrotado! Mario ganha {inimigo.pontos} pontos.")
            stdscr.refresh()
            curses.napms(2000)  # Espera 2 segundos para dar tempo de ver a mensagem
            # Marca a posição com 'X' após a batalha
            mapa[inimigo.posicao[0]][inimigo.posicao[1]] = 'X'
            return True  # Retorna para o jogo normal, sem reiniciar o turno

        
        # Se Mario perdeu toda a vida
        if mario.vida <= 0:
            stdscr.addstr(10, 0, "Mario perdeu toda a sua vida. Game Over!")
            stdscr.refresh()
            curses.napms(2000)  # Espera 2 segundos para dar tempo de ver a mensagem

            music_channel.stop()

            # Tocar a música de morte
            death_music_path = os.path.join(os.path.dirname(__file__), "death.mp3")
            pygame.mixer.music.load(death_music_path)
            pygame.mixer.music.play()

            # Perguntar ao jogador se ele quer continuar
            stdscr.clear()
            stdscr.addstr(0, 0, "Deseja continuar o jogo? Sim [S], Não [N]")
            stdscr.refresh()

            # Aguarda a resposta
            while True:
                key = stdscr.getch()

                if key == ord('s') or key == ord('S'):
                    if mario.salvou_checkpoint:
                        mario.posicao = mario.checkpoint[:]  # Voltar para o checkpoint em [3, 2]
                        mario.vida = 100  # Restaurar a vida
                        mario.pontos = 0  # Resetar os pontos
                        # Alterar a posição do inimigo para 'I' (indicando que o inimigo será reposicionado)
                        mapa[inimigo.posicao[0]][inimigo.posicao[1]] = 'I'
                        pygame.mixer.music.stop()

                        # Retomar a música de fundo
                        music_path = os.path.join(os.path.dirname(__file__), "mario_music.mp3")
                        music_channel.play(pygame.mixer.Sound(music_path), loops=-1)
                        return True  # Continuar o jogo
                    else:
                        stdscr.addstr(1, 0, "Você precisa passar pelo Checkpoint para salvar o jogo!")
                        stdscr.refresh()
                        curses.napms(3000) 
                        mario.vida = 100  # Restaurar a vida
                        mario.pontos = 0
                        mario.posicao = [0,0]
                        pygame.mixer.music.stop()

                        # Retomar a música de fundo
                        music_path = os.path.join(os.path.dirname(__file__), "mario_music.mp3")
                        music_channel.play(pygame.mixer.Sound(music_path), loops=-1)
                        return True  # Finalizar o jogo 
                        
                        
                elif key == ord('n') or key == ord('N'):
                    return False  # Finalizar o jogo
                else:
                    stdscr.addstr(1, 0, "Escolha inválida! Pressione S para continuar ou N para sair.")
                    stdscr.refresh()
                    curses.napms(1000)  # Espera 1 segundo para dar tempo de ver a mensagem

        # Aguarda o jogador pressionar qualquer tecla para continuar a batalha
        stdscr.refresh()
        curses.napms(1000)  # Tempo de espera para que o jogador veja o resultado do ataque

        # Se o inimigo não foi derrotado, ele ataca Mario
        if not inimigo.derrotado:
            dano_inimigo = inimigo.atacar()
            mario.vida -= dano_inimigo
            stdscr.addstr(9, 0, f"{inimigo.nome} ataca Mario e causa {dano_inimigo} de dano!")
     

    return True

# Função para a batalha contra o Bowser
def batalha_bowser(stdscr, mario, bowser, matriz_batalha, music_channel):
    stdscr.clear()
    stdscr.addstr(0, 0, "Batalha contra Bowser! Desvie dos fogos e acerte os itens para derrotá-lo!")
    stdscr.refresh()
    curses.napms(2000)
    music_channel.stop()
    pygame.mixer.init()
    music_path = os.path.join(os.path.dirname(__file__), "bowser_music.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()

    while mario.vida > 0 and bowser.vida > 0:
        stdscr.clear()
        

        
        # Exibe a matriz de batalha
        for i in range(len(matriz_batalha)):
            for j in range(len(matriz_batalha[i])):
                if [i, j] == mario.posicao:
                    stdscr.addstr(i, j * 2, "M")  # Mario
                else:
                    stdscr.addstr(i, j * 2, matriz_batalha[i][j])  # Outros elementos
        
        stdscr.addstr(12, 0, f"Vida de Mario: {mario.vida}")
        stdscr.addstr(13, 0, f"Vida de Bowser: {bowser.vida}")
        stdscr.addstr(14, 0, "Use as setas para mover Mario. Pressione [A] para atirar um item.")
        stdscr.refresh()

        key = stdscr.getch()

        # Movimentação do Mario
        nova_posicao = mario.posicao[:]
        if key == curses.KEY_UP:
            nova_posicao[0] -= 1
        elif key == curses.KEY_DOWN:
            nova_posicao[0] += 1
        elif key == curses.KEY_LEFT:
            nova_posicao[1] -= 1
        elif key == curses.KEY_RIGHT:
            nova_posicao[1] += 1
        elif key == ord('a') or key == ord('A'):
            # Mario atira um item (causa dano ao Bowser)
            dano = 20
            bowser.vida -= dano
            stdscr.addstr(15, 0, f"Mario atirou um item! Causou {dano} de dano ao Bowser!")
            stdscr.refresh()
            curses.napms(1000)
            continue

        # Verifica se a nova posição é válida
        if 0 <= nova_posicao[0] < 12 and 0 <= nova_posicao[1] < 12:
            mario.posicao = nova_posicao

        # Verifica se Mario acertou um item
        if matriz_batalha[mario.posicao[0]][mario.posicao[1]] == 'I':
            stdscr.addstr(15, 0, "Mario acertou um item! Causou 30 de dano ao Bowser!")
            bowser.vida -= 30
            matriz_batalha[mario.posicao[0]][mario.posicao[1]] = '.'  # Remove o item
            stdscr.refresh()
            curses.napms(1000)

        # Verifica se Mario foi atingido por um fogo
        if matriz_batalha[mario.posicao[0]][mario.posicao[1]] == 'F':
            stdscr.addstr(15, 0, "Mario foi atingido por um fogo! Perdeu 20 de vida!")
            mario.vida -= 20
            matriz_batalha[mario.posicao[0]][mario.posicao[1]] = '.'  # Remove o fogo
            stdscr.refresh()
            curses.napms(1000)

        # Move os fogos na matriz
        mover_fogos(matriz_batalha)

        # Verifica se Bowser foi derrotado
        if bowser.vida <= 0:
            stdscr.addstr(16, 0, "Bowser foi derrotado! Mario venceu!")
            stdscr.refresh()
            curses.napms(2000)
            return True  # Retorna True para indicar vitória

        # Verifica se Mario foi derrotado
        if mario.vida <= 0:
            stdscr.addstr(16, 0, "Mario foi derrotado por Bowser...")
            stdscr.refresh()
            curses.napms(2000)
            return False  # Retorna False para indicar derrota

    return True



# Função para iniciar o jogo
def jogo(stdscr):
    curses.curs_set(0)  # Desabilitar o cursor
    stdscr.nodelay(1)  # Não bloquear na espera de uma tecla
    stdscr.timeout(100)  # Timeout para obter uma tecla

    mapa = [[0 for _ in range(8)] for _ in range(8)]

    mario = Mario(mapa)
    fim_fase = [7, 7]  # Definição do final da fase
    inimigos = [
        Inimigo("Goomba", 50, 10, 50, mapa),
        Inimigo("Koopa Troopa", 60, 12, 75, mapa)
    ]

    cogumelo_posicao = mario.gerar_posicao_aleatoria(mapa)
    mapa[cogumelo_posicao[0]][cogumelo_posicao[1]] = 'C'  # 'C' representa o cogumelo
    cogumelo_coletado = False

    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)  # Canal 0 para música de fundo, Canal 1 para efeitos sonoros

    # Toca a música de fundo no canal 0
    music_channel = pygame.mixer.Channel(0)
    music_path = os.path.join(os.path.dirname(__file__), "mario_music.mp3")
    music_channel.play(pygame.mixer.Sound(music_path), loops=-1)  # Repete indefinidamente
    
    # Criando o mapa (matriz) 8x8
    mapa = [[0 for _ in range(8)] for _ in range(8)]
    
    # Posicionando o Bowser no final do mapa
    bowser = Bowser()
    bowser.posicao = [7, 7]  # Posição final do Bowser
    mapa[7][7] = 'B'  # Marca a posição do Bowser no mapa

    # Fase inicial: escolha da direção
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha a direção de Mario para começar a fase:")
    stdscr.addstr(1, 0, "Pressione as setas esquerda (←) ou direita (→) para escolher")
    stdscr.refresh()

    # A música começa a tocar apenas depois que a escolha da direção for feita e o mapa for exibido
    pygame.mixer.init()
    music_path = os.path.join(os.path.dirname(__file__), "mario_music.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:  # Ir para a direita
            mario.posicao = [0, 0]
            break
        elif key == curses.KEY_LEFT:  # Ir para a esquerda
            mario.posicao = [7, 0]
            break
    
    # Jogo continua após escolha da direção
    while mario.vida > 0:
        exibir_mapa(stdscr, mario, mapa)  # Exibe o mapa com Mario
        
        # Verificando se Mario chegou ao Bowser
        if mario.posicao == bowser.posicao:
            stdscr.clear()
            stdscr.addstr(0, 0, "Mario encontrou o Bowser! Prepare-se para a batalha final!")
            stdscr.refresh()
            curses.napms(2000)

            # Cria a nova matriz de batalha
            matriz_batalha = criar_matriz_batalha_bowser()
            
            # Inicia a batalha especial contra o Bowser
            # Dentro da função jogo, onde você chama batalha_bowser
            resultado_batalha = batalha_bowser(stdscr, mario, bowser, matriz_batalha, music_channel)
            
            if resultado_batalha:
                stdscr.clear()
                stdscr.addstr(0, 0, "Mario derrotou Bowser! Desculpe mas a princesa está em outro castelo!")
                stdscr.refresh()
                curses.napms(4000)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "Mario foi derrotado por Bowser...")
                stdscr.refresh()
                curses.napms(2000)

            # Fim do jogo
            music_path = os.path.join(os.path.dirname(__file__), "music_ending.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

                # Esperar até que a música termine
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            

            stdscr.clear()
            stdscr.addstr(0, 0, "Jogo finalizado!")
            stdscr.refresh()
            curses.napms(2000)
            return  # Encerra o jogo
        
        # Verificando se Mario encontrou o cogumelo
        if mario.posicao == cogumelo_posicao and not cogumelo_coletado:
            mario.vida += 50
            stdscr.addstr(10, 0, f"Mario encontrou um cogumelo! Vida aumentada para {mario.vida}!")
            stdscr.refresh()

            # Toca o som de vida no canal 1
            sound_channel = pygame.mixer.Channel(1)
            life_sound_path = os.path.join(os.path.dirname(__file__), "life.mp3")
            sound_channel.play(pygame.mixer.Sound(life_sound_path))

            curses.napms(2000)  # Espera 2 segundos para o jogador ver a mensagem

            mapa[cogumelo_posicao[0]][cogumelo_posicao[1]] = '.'  # Remove o cogumelo do mapa
            cogumelo_coletado = True
            
        key = stdscr.getch()

        if key == curses.KEY_UP:  # Mover para cima
            mario.mover("UP", mapa)
        elif key == curses.KEY_DOWN:  # Mover para baixo
            mario.mover("DOWN", mapa)
        elif key == curses.KEY_LEFT:  # Mover para esquerda
            mario.mover("LEFT", mapa)
        elif key == curses.KEY_RIGHT:  # Mover para direita
            mario.mover("RIGHT", mapa)

        # Se Mario encontrar inimigo, batalha
        for inimigo in inimigos:
            if mario.posicao == inimigo.posicao:
                batalha_ativa = turno_batalha(stdscr, mario, inimigo, mapa, music_channel)
                if not batalha_ativa:
                    return  # Sai do jogo se o jogador escolher não continuar

if __name__ == "__main__":
    curses.wrapper(jogo)