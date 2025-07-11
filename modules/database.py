import mysql.connector

# Função para fazer a conexão com o banco de dados
def getConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='projetoTCS'
    )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

# Função para criar as Tabelas dos Banco de dados
def createDatabase (conn, cursor):
    pass

# Função para popular as tabelas
def populateDatabase (conn, cursor):
    pass

# Função para inicializar o banco de dados
def inicializar_database ():
    conn, cursor = getConnection()
    createDatabase(conn, cursor)
    populateDatabase(conn, cursor)

    return conn, cursor