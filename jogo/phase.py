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



def get_phase_from_db(id_mundo):
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT DISTINCT idFase, nome FROM Fase WHERE idMundo = %s"
            cursor.execute(query, (id_mundo,))
            phases = [Fase(id_phase=row[0], name=row[1]) for row in cursor.fetchall()]
        return phases
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def choose_phase(stdscr, id_mundo):
    """Exibe a tela para o jogador escolher a fase."""

    phases = get_phase_from_db(id_mundo)

    if not phases:
        stdscr.addstr(0, 0, "Nenhuma fase disponível no banco de dados!")
        stdscr.refresh()
        stdscr.getch()
        return None

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
            return phases[chosen_index]
    

def get_blocos_by_fase(id_phase, mapa):
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT idBloco, tipo, idItem, idYoshi, idMoeda
                FROM Bloco
                WHERE idFase = %s
            """
            cursor.execute(query, (id_phase,))
            result = cursor.fetchall()

        if not result:
            return f"Nenhum bloco encontrado na fase {id_phase}."

        blocos = [Bloco(*row, mapa=mapa) for row in result]
        return blocos

    except Exception as e:
        print(f"Erro ao buscar blocos da fase {id_phase}: {e}")
        return None
    finally:
        connection.close()


def get_inimigo_by_fase(id_phase, mapa):
    """Retorna um objeto Inimigo do banco de dados com base no idFase."""
    connection = connect_to_db()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT p.nome, p.vida, p.dano, p.pontos, p.idLocal, i.tipo, i.habilidade
            FROM Personagem p
            JOIN Inimigo i ON p.idPersonagem = i.idPersonagem
            WHERE p.idLocal = %s AND p.tipoJogador = 'Inimigo'  # Corrigido para usar idLocal
            """
            cursor.execute(query, (id_phase,))  # Passando id_phase, que é o parâmetro correto
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
