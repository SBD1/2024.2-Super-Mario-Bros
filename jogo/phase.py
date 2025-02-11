from db import connect_to_db
import curses
import random

class Fase:
    def __init__(self, id_phase, name):
        self.id_phase = id_phase
        self.name = name

class Bloco:
    def __init__(self, id_bloco, tipo, id_item=None, id_yoshi=None, id_moeda=None, mapa=None):
        self.id_bloco = id_bloco
        self.tipo = tipo
        self.id_item = id_item
        self.id_yoshi = id_yoshi
        self.id_moeda = id_moeda
        self.posicao = self.gerar_posicao_aleatoria(mapa)

    def gerar_posicao_aleatoria(self, mapa):
        while True:
            x = random.randint(0, len(mapa) - 1)
            y = random.randint(0, len(mapa[0]) - 1)
            if mapa[x][y] != 'M' and mapa[x][y] != 'C':
                return [x, y]

    def __repr__(self):
        return (f"Bloco(id_bloco={self.id_bloco}, tipo='{self.tipo}', "
                f"id_item={self.id_item}, id_yoshi={self.id_yoshi}, id_moeda={self.id_moeda})")


class Inimigo:
    def __init__(self, nome, vida, dano, pontos, id_local, tipo, habilidade, mapa):
        self.nome = nome
        self.vida = vida
        self.dano = dano
        self.pontos = pontos
        self.id_local = id_local
        self.tipo = tipo
        self.habilidade = habilidade
        self.posicao = self.gerar_posicao_aleatoria(mapa)  # Posição aleatória para o inimigo
        self.derrotado = False  # Indica se o inimigo foi derrotado

    def gerar_posicao_aleatoria(self, mapa):
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


def get_phases_from_db(id_mundo):
    """Busca todas as fases de um mundo específico no banco de dados e retorna uma lista de objetos Fase."""
    connection = connect_to_db()
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT idFase, nome
                FROM Fase
                WHERE idMundo = %s
                ORDER BY idFase;
            """
            cursor.execute(query, (id_mundo,))
            result = cursor.fetchall()

        # Se não houver resultados, retorna uma lista vazia
        if not result:
            return []

        phases = [Fase(row[0], row[1]) for row in result]
        return phases

    except Exception as e:
        print(f"Erro ao buscar fases do mundo {id_mundo}: {e}")
        return []
    finally:
        connection.close()



def choose_phase(stdscr, id_mundo):
    """Exibe a tela para o jogador escolher uma fase e retorna a escolhida junto com as demais."""

    phases = get_phases_from_db(id_mundo)

    if not phases:
        stdscr.addstr(0, 0, "Nenhuma fase disponível no banco de dados!")
        stdscr.refresh()
        stdscr.getch()
        return None, []

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha em qual fase entrar:")

    for i, phase in enumerate(phases):
        stdscr.addstr(i + 1, 0, f"[{i + 1}] {phase.name}")

    stdscr.addstr(len(phases) + 2, 0, "Pressione o número correspondente para escolher.")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if ord('1') <= key < ord('1') + len(phases):
            chosen_index = key - ord('1')
            chosen_phase = phases[chosen_index]
            other_phases = [phase for i, phase in enumerate(phases) if i != chosen_index]
            return chosen_phase, other_phases 
    

def get_blocos_by_fase(id_phase, mapa):
    connection = connect_to_db()
    if not connection:
        return []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT idBloco, tipo, idItem, idYoshi, idMoeda
                FROM Bloco
                WHERE idFase = %s
            """
            cursor.execute(query, (id_phase,))
            result = cursor.fetchall()

        # Se não houver resultados, retorna uma lista vazia
        if not result:
            return []

        blocos = [Bloco(*row, mapa=mapa) for row in result]
        return blocos

    except Exception as e:
        print(f"Erro ao buscar blocos da fase {id_phase}: {e}")
        return []
    finally:
        connection.close()



def get_inimigo_by_fase(id_phase, mapa):
    """Retorna uma lista de objetos Inimigo do banco de dados com base no idFase."""
    connection = connect_to_db()
    if not connection:
        return []  # Retorna uma lista vazia em vez de None

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.nome, p.vida, p.dano, p.pontos, p.idFase, i.tipo, i.habilidade
            FROM Personagem p
            JOIN Inimigo i ON p.idPersonagem = i.idPersonagem
            WHERE p.idFase = %s AND p.tipoJogador = 'Inimigo'
            """
            cursor.execute(query, (id_phase,))  # Passando id_phase, que é o parâmetro correto
            inimigos_data = cursor.fetchall()  # Usa fetchall para obter todos os inimigos

        # Se não houver inimigos, retorna uma lista vazia
        if not inimigos_data:
            return []

        # Criando e retornando uma lista de objetos Inimigo
        inimigos = [
            Inimigo(
                nome=inimigo[0],
                vida=inimigo[1],
                dano=inimigo[2],
                pontos=inimigo[3],
                id_local=inimigo[4],
                tipo=inimigo[5],
                habilidade=inimigo[6],
                mapa=mapa
            )
            for inimigo in inimigos_data
        ]
        return inimigos

    except Exception as e:
        print(f"Erro ao buscar inimigos: {e}")
        return []  # Retorna uma lista vazia em caso de erro
    finally:
        connection.close()

def get_inimigo_from_db(id_personagem, mapa):
    """Retorna um objeto Inimigo do banco de dados com base no idPersonagem."""
    connection = connect_to_db()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.nome, p.vida, p.dano, p.pontos, p.idFase, i.tipo, i.habilidade
            FROM Personagem p
            JOIN Inimigo i ON p.idPersonagem = i.idPersonagem
            WHERE p.idPersonagem = %s AND p.tipoJogador = 'Inimigo'
            """
            cursor.execute(query, (id_personagem,))
            inimigo_data = cursor.fetchone()

        if not inimigo_data:
            return None  # Retorna None se o inimigo não for encontrado

        # Criando e retornando um objeto Inimigo
        return Inimigo(
            nome=inimigo_data[0],
            vida=inimigo_data[1],
            dano=inimigo_data[2],
            pontos=inimigo_data[3],
            id_local=inimigo_data[4],
            tipo=inimigo_data[5],
            habilidade=inimigo_data[6],
            mapa=mapa
        )

    except Exception as e:
        print(f"Erro ao buscar inimigo: {e}")
        return None
    finally:
        connection.close()