from db import connect_to_db
import curses
import random

class Local:
    def __init__(self, id_local, name, description):
        self.id = id_local
        self.name = name
        self.description = description
        self.is_final_local = False

def initial_local_by_phase(id_phase):
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT idLocal, nome, descricao FROM Local WHERE idFase = %s"
            cursor.execute(query, (id_phase,))
            locais = cursor.fetchall()

        if not locais:
            return f"Nenhum local encontrado para a fase com idFase = {id_phase}."
        
        local_aleatorio = random.choice(locais)
        id_local, nome_local, descricao_local = local_aleatorio
        local = Local(id_local=id_local, name=nome_local, description=descricao_local)

        return local
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()


def exploration_local(stdscr, id_phase, local_phase, id_character):
    stdscr.clear()
    stdscr.addstr(0, 0, "Escolha uma direção para se mover (setas para mover):")
    stdscr.refresh()

    direction = stdscr.getch()
    new_local = local_phase
    encounter = None

    if direction == curses.KEY_UP:
        new_local = move_player_by_direction("sul", id_phase, id_character) 
        encounter = get_encounter_by_local(new_local)
    elif direction == curses.KEY_DOWN:
        new_local = move_player_by_direction("norte", id_phase, id_character) 
        encounter = get_encounter_by_local(new_local)
    elif direction == curses.KEY_LEFT:
        new_local = move_player_by_direction("oeste", id_phase, id_character)
        encounter = get_encounter_by_local(new_local)
    elif direction == curses.KEY_RIGHT:
        new_local = move_player_by_direction("leste", id_phase, id_character)
        encounter = get_encounter_by_local(new_local)
    else:
        stdscr.addstr(3, 0, "Direção inválida")

    if encounter and 'Checkpoint' in encounter:
        new_local.is_final_local = True
    
    stdscr.refresh()
    stdscr.getch()

    return new_local, encounter

def move_player_by_direction(direction, id_phase, id_character):
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = "SELECT idLocal, nome, descricao FROM Local WHERE idFase = %s AND regiao = %s"
            cursor.execute(query, (id_phase, direction))
            locais = cursor.fetchall()

        if not locais:
            return f"Nenhum local encontrado para a fase com idFase = {id_phase}."
        
        local_aleatorio = random.choice(locais)
        id_local, nome_local, descricao_local = local_aleatorio

        with connection.cursor() as cursor:
            update_query = "UPDATE Personagem SET idLocal = %s WHERE idPersonagem = %s"
            cursor.execute(update_query, (id_local, id_character))
            connection.commit()

        local = Local(id_local=id_local, name=nome_local, description=descricao_local)

        return local
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return []
    finally:
        connection.close()

def get_encounter_by_local(local_phase):
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT idBloco, idPersonagem, idLoja, idCheckpoint
                FROM Local
                WHERE idLocal = %s
            """
            cursor.execute(query, (local_phase.id,))
            result = cursor.fetchone()

        if not result:
            return f"Nenhuma entidade encontrada no local {local_phase.nome}."
        
        id_bloco, id_personagem, id_loja, id_checkpoint = result
        tipo_personagem = None

        if id_personagem:
            with connection.cursor() as cursor:
                query_tipo = "SELECT tipojogador FROM Personagem WHERE idPersonagem = %s"
                cursor.execute(query_tipo, (id_personagem,))
                tipo_result = cursor.fetchone()
                if tipo_result:
                    tipo_personagem = tipo_result[0]

        encounter = {
            "Bloco": id_bloco if id_bloco else None,
            "Personagem": {
                "id": id_personagem,
                "tipo": tipo_personagem
            } if id_personagem else None,
            "Loja": id_loja if id_loja else None,
            "Checkpoint": id_checkpoint if id_checkpoint else None,
        }

        return encounter

    except Exception as e:
        print(f"Erro ao buscar entidades do local: {e}")
        return None
    finally:
        connection.close()