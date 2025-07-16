from src.data.data import dados_tratados
from src.database.inicializar_database import inicializar_database

dados = dados_tratados()

conn, cursor = inicializar_database()