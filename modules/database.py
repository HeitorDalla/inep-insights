import mysql.connector

# Função para fazer a conexão com o banco de dados
def getConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='m!070368M',
        database='escola_db'
    )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

# Função para criar as tabelas do banco de dados
def createDatabase (conn, cursor): 

    """
    Executa todos os comandos DDL para criar o banco e as tabelas normalizadas.
    """

    cursor.execute("CREATE DATABASE IF NOT EXISTS escola_db;")
    cursor.execute("USE escola_db;")

    # Tabela de regiões (ex: Sul, Norte, Nordeste, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regiao (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_REGIAO VARCHAR(50) NOT NULL
        );
    """
    )

    # Tabela de UFs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uf (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_UF VARCHAR(50) NOT NULL,
            regiao_id INT NOT NULL,
            FOREIGN KEY (regiao_id) REFERENCES regiao(id)
        );
    """
    )

    # Tabela de Municípios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS municipio (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_MUNICIPIO VARCHAR(100) NOT NULL,
            uf_id INT NOT NULL,
            FOREIGN KEY (uf_id) REFERENCES uf(id)
        );
    """
    )

    # Tabela de Localização (1 - Urbana | 2 - Rural)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipo_localizacao (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            TP_LOCALIZACAO INT NOT NULL,
            descricao VARCHAR(50) AS (
                CASE
                    WHEN TP_LOCALIZACAO = 1 THEN 'Urbana'
                    WHEN TP_LOCALIZACAO = 2 THEN 'Rural'
                ELSE 'Desconhecido'
                END
            ) STORED NOT NULL
        );
    """
    )

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS tipo_localizacao_diferenciada (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         codigo INT,
    #         descricao VARCHAR(100)
    #     );
    # """
    # )

    # Tabela de Localização (1- Ativa | 2- Inativa | 3 ou 4 - Extinta)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tipo_situacao (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            TP_SITUACAO_FUNCIONAMENTO INT NOT NULL,
            descricao VARCHAR(50) AS (
                CASE
                    WHEN TP_SITUACAO_FUNCIONAMENTO = 1 THEN 'Ativa'
                    WHEN TP_SITUACAO_FUNCIONAMENTO = 2 THEN 'Inativa'
                    WHEN TP_SITUACAO_FUNCIONAMENTO IN (3,4) THEN 'Extinta'
                    ELSE 'Desconhecido'
                END
                ) STORED NOT NULL
        );
    """
    )

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS tipo_dependencia (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         codigo INT,
    #         descricao VARCHAR(50)
    #     );
    # """
    # )

    # Tabela principal: Escola (união de todas as outras entidades/tabelas) 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escola (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_ENTIDADE VARCHAR(100) NOT NULL,
            municipio_id INT NOT NULL,
            tp_localizacao_id INT NOT NULL,
            tp_situacao_id INT NOT NULL,
            FOREIGN KEY (municipio_id) REFERENCES municipio(id),
            FOREIGN KEY (tp_localizacao_id) REFERENCES tipo_localizacao(id),
            FOREIGN KEY (tp_situacao_id) REFERENCES tipo_situacao(id)
        );
    """
    )

    # Tabelas de Saneamento Básico
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saneamento_basico (
            escola_id INT PRIMARY KEY NOT NULL,
            IN_AGUA_POTAVEL BOOL NOT NULL,
            IN_AGUA_INEXISTENTE BOOL NOT NULL,
            IN_AGUA_POCO_ARTESIANO BOOL NOT NULL,
            IN_AGUA_REDE_PUBLICA BOOL NOT NULL,
            IN_ESGOTO_INEXISTENTE BOOL NOT NULL,
            IN_ENERGIA_INEXISTENTE BOOL NOT NULL,
            IN_LIXO_SERVICO_COLETA BOOL NOT NULL,
            IN_ENERGIA_REDE_PUBLICA BOOL NOT NULL,
            IN_ESGOTO_REDE_PUBLICA BOOL NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabelas de Infraestrutura
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS infraestrutura (
            escola_id INT PRIMARY KEY NOT NULL,
            IN_PATIO_COBERTO BOOL NOT NULL,
            IN_BIBLIOTECA BOOL NOT NULL,
            IN_LABORATORIO_CIENCIAS BOOL NOT NULL,
            IN_LABORATORIO_INFORMATICA BOOL NOT NULL,
            IN_QUADRA_ESPORTES BOOL NOT NULL,
            IN_PARQUE_INFANTIL BOOL NOT NULL,
            IN_SALA_PROFESSOR BOOL NOT NULL,
            IN_COZINHA BOOL NOT NULL,
            IN_REFEITORIO BOOL NOT NULL,
            IN_ALMOXARIFADO BOOL NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabelas de Conectividade (materiais tecnológicos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conectividade (
            escola_id INT PRIMARY KEY NOT NULL,
            IN_INTERNET BOOL NOT NULL,
            IN_EQUIP_TV INT NOT NULL,
            QT_EQUIP_MULTIMIDIA INT NOT NULL,
            QT_DESKTOP_ALUNO INT NOT NULL,
            QT_TABLET_ALUNO INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabelas do Corpo-docente
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corpo_docente (
            escola_id INT PRIMARY KEY NOT NULL,
            QT_PROF_BIBLIOTECARIO INT NOT NULL,
            QT_PROF_PEDAGOGIA INT NOT NULL,
            QT_PROF_SAUDE INT NOT NULL,
            QT_PROF_PSICOLOGO INT NOT NULL,
            QT_PROF_ADMINISTRATIVOS INT NOT NULL,
            QT_PROF_SERVICOS_GERAIS INT NOT NULL,
            QT_PROF_SEGURANCA INT NOT NULL,
            QT_PROF_GESTAO INT NOT NULL,
            QT_PROF_ASSIST_SOCIAL INT NOT NULL,
            QT_PROF_NUTRICIONISTA INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabelas das Matrículas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matriculas (
            escola_id INT PRIMARY KEY NOT NULL,
            QT_MAT_INF INT NOT NULL,
            QT_MAT_FUND INT NOT NULL,
            QT_MAT_MED INT NOT NULL,
            QT_MAT_EJA INT NOT NULL,
            QT_MAT_ESP INT NOT NULL,
            QT_MAT_BAS_FEM INT NOT NULL,
            QT_MAT_BAS_MASC INT NOT NULL,
            QT_MAT_BAS_BRANCA INT NOT NULL,
            QT_MAT_BAS_PRETA INT NOT NULL,
            QT_MAT_BAS_PARDA INT NOT NULL,
            QT_MAT_BAS_AMARELA INT NOT NULL,
            QT_MAT_BAS_INDIGENA INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabelas dos Insumos (alimentação e materiais pedagógicos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            escola_id INT PRIMARY KEY NOT NULL,
            IN_ALIMENTACAO BOOL NOT NULL,
            IN_MATERIAL_PED_CIENTIFICO BOOL NOT NULL,
            IN_MATERIAL_PED_ARTISTICAS BOOL NOT NULL,
            IN_MATERIAL_PED_DESPORTIVA BOOL NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

    # Tabela da Quantidade de Transporte Público (geral)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transporte (
            escola_id INT PRIMARY KEY NOT NULL,
            QT_TRANSP_PUBLICO INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """
    )

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