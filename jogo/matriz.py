import random

def gera_matriz(linhas=8, colunas=8):
    """
    Função para gerar uma matriz do mapa do jogo.
    A matriz será preenchida com espaços vazios, inimigos, blocos, e outros elementos.
    
    :param linhas: Número de linhas da matriz
    :param colunas: Número de colunas da matriz
    :return: matriz gerada com os elementos do jogo
    """
    # Definir o mapa inicial, preenchendo com espaços vazios '.'
    matriz = [['.' for _ in range(colunas)] for _ in range(linhas)]

    # # Colocar o Mario (M) em uma posição aleatória
    # mario_x = random.randint(0, linhas - 1)
    # mario_y = random.randint(0, colunas - 1)
    # matriz[mario_x][mario_y] = 'M'  # 'M' representa o Mario

    # # Adicionar inimigos aleatórios (I) na matriz
    # num_inimigos = 2  # Definindo o número de inimigos
    # for _ in range(num_inimigos):
    #     inimigo_x = random.randint(0, linhas - 1)
    #     inimigo_y = random.randint(0, colunas - 1)
    #     while matriz[inimigo_x][inimigo_y] != '.':  # Garantir que o inimigo não sobrescreva outro objeto
    #         inimigo_x = random.randint(0, linhas - 1)
    #         inimigo_y = random.randint(0, colunas - 1)
    #     matriz[inimigo_x][inimigo_y] = 'I'  # 'I' representa o Inimigo

    # # Adicionar blocos (B) em posições aleatórias
    # num_blocos = 4  # Definir o número de blocos
    # for _ in range(num_blocos):
    #     bloco_x = random.randint(0, linhas - 1)
    #     bloco_y = random.randint(0, colunas - 1)
    #     while matriz[bloco_x][bloco_y] != '.':  # Garantir que o bloco não sobrescreva outro objeto
    #         bloco_x = random.randint(0, linhas - 1)
    #         bloco_y = random.randint(0, colunas - 1)
    #     matriz[bloco_x][bloco_y] = 'B'  # 'B' representa o Bloco

    # # Adicionar cogumelos (C) em posições aleatórias
    # cogumelo_x = random.randint(0, linhas - 1)
    # cogumelo_y = random.randint(0, colunas - 1)
    # while matriz[cogumelo_x][cogumelo_y] != '.':  # Garantir que o cogumelo não sobrescreva outro objeto
    #     cogumelo_x = random.randint(0, linhas - 1)
    #     cogumelo_y = random.randint(0, colunas - 1)
    # matriz[cogumelo_x][cogumelo_y] = 'C'  # 'C' representa o Cogumelo

    # # Você pode adicionar mais elementos, como o Bowser (B), checkpoints, etc.

    return matriz
