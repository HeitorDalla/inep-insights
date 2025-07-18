# Importações necessárias para inicialização do banco de dados
from src.database.get_connection import get_connection
from src.database.create_database import create_database
from src.database.populate_database import populate_database

# Função para inicializar o banco de dados
def inicializar_database ():
    conn, cursor = get_connection()
    create_database(conn, cursor)
    populate_database(conn, cursor)

    return conn, cursor