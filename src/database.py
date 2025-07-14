import mysql.connector
from src.data import dados_tratados

# Função para fazer a conexão com o banco de dados
def getConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='database_projeto_tcs'
    )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

# Função para criar as tabelas do banco de dados
def createDatabase (conn, cursor): 

    """
    Executa todos os comandos DDL para criar o banco e as tabelas normalizadas.
    """

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

    conn.commit()

# Função para popular as tabelas
def populateDatabase (conn, cursor):
    # Selecionar todas as tabelas do banco de dados
    tabelas = [
        "regiao", "uf", "municipio", "tipo_localizacao", "tipo_situacao",
        "escola", "saneamento_basico", "infraestrutura", "conectividade",
        "corpo_docente", "matriculas", "insumos", "transporte"
    ]

    # Verificar algum dado ja existente
    for tabela in tabelas:
        cursor.execute(f'SELECT COUNT(*) FROM {tabela}')
        if list(cursor.fetchone().values())[0] > 0:
            return
        
    # Dados tratados
    df = dados_tratados()

    # 2. Dimensão Regiões
    for regiao in df['NO_REGIAO'].unique():
        cursor.execute(
            "INSERT IGNORE INTO regiao (NO_REGIAO) VALUES (%s)", # o IGNORE evita duplicatas
            (regiao.strip(),)
        )

    conn.commit()
    cursor.execute("SELECT id, NO_REGIAO FROM regiao")
    reg_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 3. Dimensão UFs
    for uf, reg in df[['NO_UF','NO_REGIAO']].drop_duplicates().values:
        reg_id = reg_map[reg]
        cursor.execute(
            "INSERT IGNORE INTO uf (NO_UF, regiao_id) VALUES (%s, %s)",
            (uf.strip(), reg_id)
        )

    conn.commit()
    cursor.execute("SELECT id, NO_UF FROM uf")
    uf_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 4. Dimensão Municípios
    for muni, uf in df[['NO_MUNICIPIO','NO_UF']].drop_duplicates().values:
        uf_id = uf_map[uf]
        cursor.execute(
            "INSERT IGNORE INTO municipio (NO_MUNICIPIO, uf_id) VALUES (%s, %s)",
            (muni, uf_id)
        )

    conn.commit()
    cursor.execute("SELECT id, NO_MUNICIPIO FROM municipio")
    muni_map = {nome: id_ for id_, nome in cursor.fetchall()}

    # 5. Mapas estáticos para localização e situação
    cursor.execute("SELECT id, TP_LOCALIZACAO FROM tipo_localizacao")
    loc_map = {tp: id_ for id_, tp in cursor.fetchall()}

    cursor.execute("SELECT id, TP_SITUACAO_FUNCIONAMENTO FROM tipo_situacao")
    sit_map = {tp: id_ for id_, tp in cursor.fetchall()}

    # 6. Inserir registros em escola e tabelas filhas
    for _, row in df.iterrows():
        # 6.1 escola
        cursor.execute(
            """INSERT INTO escola
               (NO_ENTIDADE, municipio_id, tp_localizacao_id, tp_situacao_id)
               VALUES (%s, %s, %s, %s)""",
            (
                row['NO_ENTIDADE'],
                muni_map[row['NO_MUNICIPIO']],
                loc_map[int(row['TP_LOCALIZACAO'])],
                sit_map[int(row['TP_SITUACAO_FUNCIONAMENTO'])]
            )
        )
        escola_id = cursor.lastrowid
        conn.commit()

        # 6.2 saneamento_basico
        cursor.execute(
            """INSERT INTO saneamento_basico
               (escola_id, IN_AGUA_POTAVEL, IN_AGUA_REDE_PUBLICA, IN_AGUA_POCO_ARTESIANO,
                IN_AGUA_INEXISTENTE, IN_ENERGIA_REDE_PUBLICA, IN_ENERGIA_INEXISTENTE,
                IN_ESGOTO_REDE_PUBLICA, IN_ESGOTO_INEXISTENTE, IN_LIXO_SERVICO_COLETA)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                escola_id,
                bool(row['IN_AGUA_POTAVEL']),
                bool(row['IN_AGUA_REDE_PUBLICA']),
                bool(row['IN_AGUA_POCO_ARTESIANO']),
                bool(row['IN_AGUA_INEXISTENTE']),
                bool(row['IN_ENERGIA_REDE_PUBLICA']),
                bool(row['IN_ENERGIA_INEXISTENTE']),
                bool(row['IN_ESGOTO_REDE_PUBLICA']),
                bool(row['IN_ESGOTO_INEXISTENTE']),
                bool(row['IN_LIXO_SERVICO_COLETA'])
            )
        )

        # 6.3 infraestrutura
        cursor.execute(
            """INSERT INTO infraestrutura
               (escola_id, IN_ALMOXARIFADO, IN_BIBLIOTECA, IN_COZINHA,
                IN_LABORATORIO_CIENCIAS, IN_LABORATORIO_INFORMATICA,
                IN_PATIO_COBERTO, IN_PARQUE_INFANTIL, IN_QUADRA_ESPORTES,
                IN_REFEITORIO, IN_SALA_PROFESSOR)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                escola_id,
                bool(row['IN_ALMOXARIFADO']),
                bool(row['IN_BIBLIOTECA']),
                bool(row['IN_COZINHA']),
                bool(row['IN_LABORATORIO_CIENCIAS']),
                bool(row['IN_LABORATORIO_INFORMATICA']),
                bool(row['IN_PATIO_COBERTO']),
                bool(row['IN_PARQUE_INFANTIL']),
                bool(row['IN_QUADRA_ESPORTES']),
                bool(row['IN_REFEITORIO']),
                bool(row['IN_SALA_PROFESSOR'])
            )
        )

        # 6.4 conectividade
        cursor.execute(
            """INSERT INTO conectividade
               (escola_id, IN_INTERNET, IN_EQUIP_TV, QT_EQUIP_MULTIMIDIA)
               VALUES (%s, %s, %s, %s)""",
            (
                escola_id,
                bool(row['IN_INTERNET']),
                int(row['IN_EQUIP_TV']),
                int(row['QT_EQUIP_MULTIMIDIA'])
            )
        )

        # 6.5 corpo_docente
        cursor.execute(
            """INSERT INTO corpo_docente
               (escola_id, QT_PROF_BIBLIOTECARIO, QT_PROF_PEDAGOGIA, QT_PROF_SAUDE,
                QT_PROF_PSICOLOGO, QT_PROF_ADMINISTRATIVOS, QT_PROF_SERVICOS_GERAIS,
                QT_PROF_SEGURANCA, QT_PROF_GESTAO, QT_PROF_ASSIST_SOCIAL, QT_PROF_NUTRICIONISTA)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                escola_id,
                int(row['QT_PROF_BIBLIOTECARIO']),
                int(row['QT_PROF_PEDAGOGIA']),
                int(row['QT_PROF_SAUDE']),
                int(row['QT_PROF_PSICOLOGO']),
                int(row['QT_PROF_ADMINISTRATIVOS']),
                int(row['QT_PROF_SERVICOS_GERAIS']),
                int(row['QT_PROF_SEGURANCA']),
                int(row['QT_PROF_GESTAO']),
                int(row['QT_PROF_ASSIST_SOCIAL']),
                int(row['QT_PROF_NUTRICIONISTA'])
            )
        )

        # 6.6 matriculas
        cursor.execute(
            """INSERT INTO matriculas
               (escola_id, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_EJA,
                QT_MAT_ESP, QT_MAT_BAS_FEM, QT_MAT_BAS_MASC, QT_MAT_BAS_BRANCA,
                QT_MAT_BAS_PRETA, QT_MAT_BAS_PARDA, QT_MAT_BAS_AMARELA,
                QT_MAT_BAS_INDIGENA)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                escola_id,
                int(row['QT_MAT_INF']),
                int(row['QT_MAT_FUND']),
                int(row['QT_MAT_MED']),
                int(row['QT_MAT_EJA']),
                int(row['QT_MAT_ESP']),
                int(row['QT_MAT_BAS_FEM']),
                int(row['QT_MAT_BAS_MASC']),
                int(row['QT_MAT_BAS_BRANCA']),
                int(row['QT_MAT_BAS_PRETA']),
                int(row['QT_MAT_BAS_PARDA']),
                int(row['QT_MAT_BAS_AMARELA']),
                int(row['QT_MAT_BAS_INDIGENA'])
            )
        )

        # 6.7 insumos
        cursor.execute(
            """INSERT INTO insumos
               (escola_id, IN_ALIMENTACAO, IN_MATERIAL_PED_CIENTIFICO,
                IN_MATERIAL_PED_ARTISTICAS, IN_MATERIAL_PED_DESPORTIVA)
               VALUES (%s, %s, %s, %s, %s)""",
            (
                escola_id,
                bool(row['IN_ALIMENTACAO']),
                bool(row['IN_MATERIAL_PED_CIENTIFICO']),
                bool(row['IN_MATERIAL_PED_ARTISTICAS']),
                bool(row['IN_MATERIAL_PED_DESPORTIVA'])
            )
        )

        # 6.8 transporte
        cursor.execute(
            "INSERT INTO transporte (escola_id, QT_TRANSP_PUBLICO) VALUES (%s, %s)",
            (escola_id, int(row['QT_TRANSP_PUBLICO']))
        )

    conn.commit()

# Função para inicializar o banco de dados
def inicializar_database ():
    conn, cursor = getConnection()
    createDatabase(conn, cursor)
    populateDatabase(conn, cursor)

    return conn, cursor