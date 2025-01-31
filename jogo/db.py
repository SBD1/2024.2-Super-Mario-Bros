import psycopg2

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="supermario",
            user="root",
            password="123456",
            host="localhost",
            port="5432"
        )
        print("Conectado ao banco de dados!")
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
