import pygame
import pyfiglet
import time
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    terminal_width = os.get_terminal_size().columns
    for line in text.split('\n'):
        print(line.center(terminal_width))

def print_centered_with_font(text, font):
    formatted_text = pyfiglet.figlet_format(text, font=font)
    print_centered(formatted_text)

# Inicializa o pygame apenas para o áudio
pygame.mixer.init()

# Carrega e toca a música de fundo
# pygame.mixer.music.load("final.mp3")  # Substitua pelo caminho do seu arquivo de áudio
# pygame.mixer.music.play(-1)  # -1 faz a música repetir indefinidamente

# Limpa o terminal
clear_terminal()

# Exibe o título "FIM DO JOGO" com pyfiglet em uma fonte estilizada
print_centered_with_font("FIM DO JOGO", "big")

# Exibe as informações de pontos, vida e moedas de forma destacada
print_centered("═" * 40)
print_centered("PONTOS: 1000")
print_centered("VIDA: 3")
print_centered("MOEDAS: 50")
print_centered("═" * 40)
print("\n")
print_centered("PRESSIONE ENTER PARA FINALIZAR O JOGO")

# Aguarda o usuário pressionar qualquer tecla para encerrar o jogo
input()
pygame.mixer.music.stop()