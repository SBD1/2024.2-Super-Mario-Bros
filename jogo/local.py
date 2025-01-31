from db import connect_to_db
import curses

class Local:
    def __init__(self, id_local, name, description):
        self.id_local = id_local
        self.name = name
        self.description = description

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

    return new_local, 

def move_player(local_phase, direction, character):
    if direction == "norte":
        new_local = get_local_phase_by_direction()
        encounter = get_encount_by_direction()
    if direction == "sul":
        new_local = get_local_phase_by_direction()        
        encounter = get_encount_by_direction()
    
    # Atualizar em sql a nova posição do jogador 

    return new_local, encounter