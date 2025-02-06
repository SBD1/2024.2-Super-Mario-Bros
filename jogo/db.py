import psycopg2


def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="supermario",
            user="dba",
            password="senha_dba",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
