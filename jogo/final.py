import pygame
import pyfiglet
import os
from db import connect_to_db

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    terminal_width = os.get_terminal_size().columns
    for line in text.split('\n'):
        print(line.center(terminal_width))

def print_centered_with_font(text, font):
    formatted_text = pyfiglet.figlet_format(text, font=font)
    print_centered(formatted_text)

def exibir_fim_de_jogo(id_jogador):
    connection = connect_to_db()
    if not connection:
        print("Não foi possível conectar ao banco de dados.")
        return

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT nome, pontos, vida, moedas
                FROM jogadores
                WHERE idJogador = %s
            """
            cursor.execute(query, (id_jogador,))
            jogador_data = cursor.fetchone()

        if not jogador_data:
            print("Jogador não encontrado!")
            return

        nome_jogador, pontos_jogador, vida_jogador, moedas_jogador = jogador_data

        # Inicializa o pygame apenas para o áudio
        pygame.mixer.init()

        # Carrega e toca a música de fundo
        pygame.mixer.music.load("final.mp3")  # Substitua pelo caminho do seu arquivo de áudio
        pygame.mixer.music.play(-1)  # -1 faz a música repetir indefinidamente

        # Limpa o terminal
        clear_terminal()

        # Exibe o título "FIM DO JOGO" com pyfiglet em uma fonte estilizada
        print_centered_with_font("FIM DO JOGO", "big")

        # Exibe as informações do jogador de forma destacada
        print_centered("═" * 40)
        print_centered(f"NOME: {nome_jogador}")
        print_centered(f"PONTOS: {pontos_jogador}")
        print_centered(f"VIDA: {vida_jogador}")
        print_centered(f"MOEDAS: {moedas_jogador}")
        print_centered("═" * 40)
        print("\n")
        print_centered("PRESSIONE ENTER PARA FINALIZAR O JOGO")

        # Aguarda o usuário pressionar qualquer tecla para encerrar o jogo
        input()
        pygame.mixer.music.stop()

    except Exception as e:
        print(f"Erro ao buscar dados do jogador: {e}")
    finally:
        connection.close()

# Exemplo de uso
if __name__ == "__main__":
    id_jogador = 1  # Substitua pelo ID do jogador que deseja exibir
    exibir_fim_de_jogo(id_jogador)
