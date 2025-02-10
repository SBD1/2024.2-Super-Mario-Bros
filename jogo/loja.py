import random
from db import connect_to_db
import curses

class Item:
    def __init__(self, id_item, tipo, efeito, duracao, raridade, quantidade):
        self.id_item = id_item
        self.tipo = tipo
        self.efeito = efeito
        self.duracao = duracao
        self.raridade = raridade
        self.quantidade = quantidade
        self.preco = self.definir_preco()
    
    def definir_preco(self):
        precos_base = {
            "comum": 10,
            "incomum": 20,
            "raro": 50,
            "lendário": 100
        }
        return precos_base.get(self.raridade.lower(), 10)

    def __repr__(self):
        return f"Item(id_item={self.id_item}, tipo={self.tipo}, efeito={self.efeito}, duracao={self.duracao}, raridade={self.raridade}, quantidade={self.quantidade}, preco={self.preco})"

class Loja:
    def __init__(self, id_loja, name, items=[]):
        self.id = id_loja
        self.name = name
        self.items = items

    def __repr__(self):
        return f"Loja(id={self.id}, name={self.name}, items={self.items})"

def get_loja_with_items(id_loja):
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            loja_query = "SELECT idLoja, nome FROM Loja WHERE idLoja = %s"
            cursor.execute(loja_query, (id_loja,))
            loja_data = cursor.fetchone()
            
            if not loja_data:
                return f"Nenhuma loja encontrada com idLoja = {id_loja}."

            item_query = """
                SELECT I.idItem, I.tipo, I.efeito, I.duracao, I.raridade, LI.quantidade
                FROM LojaItem LI
                JOIN Item I ON LI.idItem = I.idItem
                WHERE LI.idLoja = %s
            """
            cursor.execute(item_query, (id_loja,))
            items_data = cursor.fetchall()
        
        items = [Item(*item) for item in items_data] if items_data else []
        loja = Loja(loja_data[0], loja_data[1], items)
        return loja
    except Exception as e:
        print(f"Erro ao executar consulta: {e}")
        return None
    finally:
        connection.close()

def get_player_inventory(player_id):
    connection = connect_to_db()
    if not connection:
        return []
    
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT I.idItem, I.tipo, I.efeito, I.duracao, I.raridade, Inv.quantidade
            FROM Inventario Inv
            JOIN Item I ON Inv.idItem = I.idItem
            WHERE Inv.idpersonagem = %s
            """
            cursor.execute(query, (player_id,))
            items_data = cursor.fetchall()
        
        return [Item(*item) for item in items_data] if items_data else []
    except Exception as e:
        print(f"Erro ao buscar inventário: {e}")
        return []
    finally:
        connection.close()

def comprar_item(stdscr, player, loja):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Bem-vindo à {loja.name}!")
    stdscr.addstr(1, 0, "Itens disponíveis para compra:")
    row = 2
    for idx, item in enumerate(loja.items):
        stdscr.addstr(row, 0, f"{idx + 1}. {item.tipo} ({item.raridade}) - {item.efeito} | Duração: {item.duracao} | Quantidade: {item.quantidade} | Preço: {item.preco}")
        row += 1
    stdscr.addstr(row, 0, "Escolha um item pelo número ou pressione 'q' para sair:")
    stdscr.refresh()
    
    choice = stdscr.getch()
    if choice == ord('q'):
        return
    
    choice = int(chr(choice)) - 1
    if 0 <= choice < len(loja.items):
        item_escolhido = loja.items[choice]
        adicionar_ao_inventario(player, item_escolhido)
        loja.items.pop(choice)
        stdscr.addstr(row + 1, 0, f"Você comprou {item_escolhido.tipo}!")
    else:
        stdscr.addstr(row + 1, 0, "Escolha inválida.")
    stdscr.refresh()
    stdscr.getch()

def vender_item(stdscr, player_id, loja):
    inventario = get_player_inventory(player_id)
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Seu inventário:")
    row = 1
    for idx, item in enumerate(inventario):
        stdscr.addstr(row, 0, f"{idx + 1}. {item.tipo} ({item.raridade}) - Preço de venda: {item.preco // 2}")
        row += 1
    stdscr.addstr(row, 0, "Escolha um item para vender pelo número ou pressione 'q' para sair:")
    stdscr.refresh()
    
    choice = stdscr.getch()
    if choice == ord('q'):
        return
    
    choice = int(chr(choice)) - 1
    if 0 <= choice < len(inventario):
        item_vendido = inventario[choice]
        remover_do_inventario(player_id, item_vendido.id_item)
        adicionar_ao_loja(loja, item_vendido)
        stdscr.addstr(row + 1, 0, f"Você vendeu {item_vendido.tipo}!")
    else:
        stdscr.addstr(row + 1, 0, "Escolha inválida.")
    stdscr.refresh()
    stdscr.getch()

def remover_do_inventario(player_id, id_item):
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            delete_query = """
            DELETE FROM Inventario
            WHERE idpersonagem = %s AND idItem = %s
            """
            cursor.execute(delete_query, (player_id, id_item))
            connection.commit()
    except Exception as e:
        print(f"Erro ao remover item do inventário: {e}")
    finally:
        connection.close()

def adicionar_ao_loja(loja, item):
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            check_query = """
            SELECT quantidade
            FROM LojaItem
            WHERE idLoja = %s AND idItem = %s
            """
            cursor.execute(check_query, (loja.id, item.id_item))
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[0] + 1
                update_query = """
                UPDATE LojaItem
                SET quantidade = %s
                WHERE idLoja = %s AND idItem = %s
                """
                cursor.execute(update_query, (new_quantity, loja.id, item.id_item))
            else:
                insert_query = """
                INSERT INTO LojaItem (idLoja, idItem, quantidade)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (loja.id, item.id_item, 1))

            connection.commit()
    except Exception as e:
        print(f"Erro ao adicionar à loja: {e}")
    finally:
        connection.close()

def adicionar_ao_inventario(player, item):
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            check_query = """
            SELECT idInventario, quantidade
            FROM Inventario
            WHERE idItem = %s AND idpersonagem = %s
            """
            cursor.execute(check_query, (item.id_item, player.id))
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[1] + 1
                update_query = """
                UPDATE Inventario
                SET quantidade = %s
                WHERE idInventario = %s
                """
                cursor.execute(update_query, (new_quantity, existing_item[0]))
            else:
                insert_query = """
                INSERT INTO Inventario (quantidade, idItem, idpersonagem)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_query, (1, item.id_item, player.id))

            connection.commit()
    except Exception as e:
        print(f"Erro ao adicionar ao inventário: {e}")
    finally:
        connection.close()