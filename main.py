from src.data import dados_tratados
from src.database import inicializar_database

dados = dados_tratados()

conn, cursor = inicializar_database()
