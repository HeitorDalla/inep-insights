    # Função responsável por criar todas as tabelas do banco de dados
def create_database(conn, cursor):
    """
    Executa todos os comandos DDL para criar o banco e as tabelas normalizadas.
    """
    # 1. Criação da tabela de regiões geográficas do Brasil
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regiao (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_REGIAO VARCHAR(50) NOT NULL,
            UNIQUE KEY uq_regiao (NO_REGIAO)
        );
    """)

    # 2. Criação da tabela de Unidades Federativas (UFs), associadas a uma região
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uf (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_UF VARCHAR(50) NOT NULL,
            regiao_id INT NOT NULL,
            FOREIGN KEY (regiao_id) REFERENCES regiao(id),
            UNIQUE KEY uq_uf (NO_UF, regiao_id)
        );
    """)

    # 3. Tabela de municípios, vinculados a uma UF
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS municipio (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_MUNICIPIO VARCHAR(100) NOT NULL,
            uf_id INT NOT NULL,
            FOREIGN KEY (uf_id) REFERENCES uf(id),
            UNIQUE KEY uq_municipio (NO_MUNICIPIO, uf_id)
        );
    """)

    # 4. Tabela para representar a localização da escola: Urbana (1) ou Rural (2)
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
            ) STORED NOT NULL,
            UNIQUE KEY uq_tipo_localizacao (TP_LOCALIZACAO)
        );
    """)

    # 5. Tabela principal que representa as escolas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escola (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            NO_ENTIDADE VARCHAR(200) NOT NULL,
            DS_ENDERECO VARCHAR(200) NOT NULL,
            municipio_id INT NOT NULL,
            tp_localizacao_id INT NOT NULL,
            FOREIGN KEY (municipio_id) REFERENCES municipio(id),
            FOREIGN KEY (tp_localizacao_id) REFERENCES tipo_localizacao(id)
        );
    """)

    # 6. Tabela com informações de saneamento básico das escolas
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
    """)

    # 7. Tabela com infraestrutura física das escolas
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
            IN_ALIMENTACAO BOOL NOT NULL,
            QT_TRANSP_PUBLICO INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """)

    # 8. Tabela com informações do corpo docente e equipe técnica
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
    """)

    # 9. Tabela com dados de matrículas por etapa de ensino e perfil do aluno
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
    """)

    # 10. Tabela com insumos e materiais pedagógicos disponíveis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materiais (
            escola_id INT PRIMARY KEY NOT NULL,
            IN_MATERIAL_PED_CIENTIFICO BOOL NOT NULL,
            IN_MATERIAL_PED_ARTISTICAS BOOL NOT NULL,
            IN_MATERIAL_PED_DESPORTIVA BOOL NOT NULL,
            IN_INTERNET BOOL NOT NULL,
            QT_EQUIP_MULTIMIDIA INT NOT NULL,
            FOREIGN KEY (escola_id) REFERENCES escola(id)
        );
    """)

    # Aplica (commita) todas as criações no banco de dados
    conn.commit()