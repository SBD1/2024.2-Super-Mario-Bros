import curses 
import random
import pyfiglet  # Importando o pyfiglet
import pygame
import os

#Definindo fase final
TOTAL_MUNDOS = 3
FASES_POR_MUNDO = 3

# Definindo o personagem Mario
class Mario:
    def __init__(self):
        self.vida = 100
        self.pontos = 0
        self.posicao = [1, 1]  # Posição inicial do Mario na matriz (1, 1)
        self.checkpoint = [3, 2]  # O checkpoint fixo que sempre será 3, 2
        self.salvou_checkpoint = False  # Indica se Mario já salvou o checkpoint
        self.fase = 1
        self.mundo = 1
        
    def avancar_fase(self):
        if self.fase < FASES_POR_MUNDO:
            self.fase += 1
        else:
            print(f"Mundo {self.mundo} - Fase {self.fase}: Esta era a fase final do mundo!")
            self.fase = 1
            self.mundo += 1


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
            print(f"Mario se moveu para {self.posicao}")
            
            # Verifica se Mario passou pela posição do checkpoint
            if self.posicao == self.checkpoint and not self.salvou_checkpoint:
                self.salvou_checkpoint = True
                print("Checkpoint salvo em [3, 2]!")
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
    titulo_ascii = pyfiglet.figlet_format("FASE 1", font="slant")  # Usando a fonte "slant" como exemplo
    
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
            else:
                stdscr.addstr(mapa_inicio_y + i, mapa_inicio_x + j * 2, ".")  # Exibe '.' para as outras células
    
    stdscr.refresh()

# Função para rodar um turno de batalha
class Inimigo:
    def __init__(self, nome, vida, dano, pontos):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.pontos = pontos
        self.posicao = [3, 3]  # Exemplo de posição inicial do inimigo
        self.derrotado = False  # Indica se o inimigo foi derrotado

    def atacar(self):
        return self.dano

    def perder_vida(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.derrotado = True  # Marca como derrotado quando a vida chegar a zero

# Função para rodar um turno de batalha
def turno_batalha(stdscr, mario, inimigo, mapa):
    # Verifica se o inimigo foi derrotado antes de iniciar a batalha
    if inimigo.derrotado:
       # stdscr.addstr(5, 0, f"\n{inimigo.nome} já foi derrotado! Mario não pode enfrentar novamente.")
       ## stdscr.refresh()
      #  curses.napms(2000)  # Espera 2 segundos para o jogador ver a mensagem
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
                mario.pontos += inimigo.pontos  # Adiciona os pontos do Goomba
            elif inimigo.nome == "Koopa Troopa":
                inimigo.perder_vida(dano_pulo)  # Koopa Troopa leva o dano de 10
                stdscr.addstr(5, 0, f"{inimigo.nome} sofreu {dano_pulo} de dano pelo pulo!")
                if inimigo.vida <= 0:
                    mario.pontos += inimigo.pontos  # Adiciona os pontos do Koopa Troopa
            break

        elif key == ord('e') or key == ord('E'):  # Desviar
            mario.desviar()
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
                        return True  # Continuar o jogo
                    else:
                        stdscr.addstr(1, 0, "Você precisa passar pela posição [3, 2] para salvar o jogo!")
                        stdscr.refresh()
                        curses.napms(3000) 
                        return False  # Finalizar o jogo 
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
        
        # Se Mario perde toda a vida, a batalha termina
        if mario.vida <= 0:
            stdscr.addstr(10, 0, "Mario perdeu toda a sua vida. Game Over!")
            stdscr.refresh()
            curses.napms(2000)  # Espera 2 segundos para o jogador ver a mensagem
            break

    return True


# Função para iniciar o jogo
def jogo(stdscr):
    curses.curs_set(0)  # Desabilitar o cursor
    stdscr.nodelay(1)  # Não bloquear na espera de uma tecla
    stdscr.timeout(100)  # Timeout para obter uma tecla

    mario = Mario()
    fim_fase = [7, 7]  # Definição do final da fase
    inimigos = [
        Inimigo("Goomba", 50, 10, 50),
        Inimigo("Koopa Troopa", 75, 15, 75),
    ]
    
    # Criando o mapa (matriz) 8x8
    mapa = [[0 for _ in range(8)] for _ in range(8)]
    
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
        
        # Verificando se Mario chegou ao final da fase
        if mario.posicao == fim_fase:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Parabéns! Mario completou a fase com {mario.pontos} pontos!")
            stdscr.refresh()
            curses.napms(2000)  # Espera 2 segundos para o jogador ver a mensagem
             # Tocar a música de encerramento
            music_path = os.path.join(os.path.dirname(__file__), "music_ending.mp3")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()

            # Esperar até que a música termine
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            break  # Fim do jogo

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
                batalha_ativa = turno_batalha(stdscr, mario, inimigo, mapa)
                if not batalha_ativa:
                    break  # Sai do jogo se o jogador escolher não continuar

    stdscr.clear()
    stdscr.addstr(0, 0, "Jogo finalizado!")
    stdscr.refresh()
    curses.napms(2000)  # Espera 2 segundos para o jogador ver a mensagem



if __name__ == "__main__":
    curses.wrapper(jogo)