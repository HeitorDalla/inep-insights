from src.data.dados_tratados import dados_tratados
from src.database.inicializar_database import inicializar_database

dados = dados_tratados()

conn, cursor = inicializar_database()