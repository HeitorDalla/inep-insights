from src.data.data import dados_tratados

# Função para popular o banco de dados
def populate_database(conn, cursor):
    # 1. Carrega CSV
    df = dados_tratados()

    try:
        # 2a. Seed 'regiao'
        for reg in df['NO_REGIAO'].unique():
            cursor.execute("SELECT id FROM regiao WHERE NO_REGIAO = %s", (reg,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO regiao (NO_REGIAO) VALUES (%s)", (reg,))

        # 2b. Seed 'uf'
        # precisa do regiao_id
        cursor.execute("SELECT id, NO_REGIAO FROM regiao")
        reg_map = { r['NO_REGIAO']: r['id'] for r in cursor.fetchall() }

        for uf, reg in df[['NO_UF','NO_REGIAO']].drop_duplicates().values:
            reg_id = reg_map[reg]
            cursor.execute(
                "SELECT id FROM uf WHERE NO_UF = %s AND regiao_id = %s",
                (uf, reg_id)
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO uf (NO_UF, regiao_id) VALUES (%s, %s)",
                    (uf, reg_id)
                )

        # 2c. Seed 'municipio'
        cursor.execute("SELECT id, NO_UF FROM uf")
        uf_map = { r['NO_UF']: r['id'] for r in cursor.fetchall() }

        for muni, uf in df[['NO_MUNICIPIO','NO_UF']].drop_duplicates().values:
            uf_id = uf_map[uf]
            cursor.execute(
                "SELECT id FROM municipio WHERE NO_MUNICIPIO = %s AND uf_id = %s",
                (muni, uf_id)
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO municipio (NO_MUNICIPIO, uf_id) VALUES (%s, %s)",
                    (muni, uf_id)
                )

        # 2d. Seed 'tipo_localizacao'
        for tp in df['TP_LOCALIZACAO'].unique():
            cursor.execute(
                "SELECT id FROM tipo_localizacao WHERE TP_LOCALIZACAO = %s",
                (int(tp),)
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO tipo_localizacao (TP_LOCALIZACAO) VALUES (%s)",
                    (int(tp),)
                )

        # Reconstrói o map de situação 
        # 3. Reconstrói todos os maps
        cursor.execute("SELECT id, NO_REGIAO FROM regiao")
        reg_map = { r['NO_REGIAO']: r['id'] for r in cursor.fetchall() }

        cursor.execute("SELECT id, NO_UF FROM uf")
        uf_map = { r['NO_UF']: r['id'] for r in cursor.fetchall() }

        cursor.execute("SELECT id, NO_MUNICIPIO FROM municipio")
        muni_map = { r['NO_MUNICIPIO']: r['id'] for r in cursor.fetchall() }

        cursor.execute("SELECT id, TP_LOCALIZACAO FROM tipo_localizacao")
        loc_map = { r['TP_LOCALIZACAO']: r['id'] for r in cursor.fetchall() }

        # 4. Insere cada escola e suas tabelas filhas
        for row in df.itertuples(index=False):
            # 4a. escola
            cursor.execute(
                """INSERT INTO escola
                (NO_ENTIDADE, municipio_id, tp_localizacao_id)
                VALUES (%s, %s, %s)""",
                (
                    row.NO_ENTIDADE,
                    muni_map[row.NO_MUNICIPIO],
                    loc_map[int(row.TP_LOCALIZACAO)]
                )
            )
            escola_id = cursor.lastrowid

            # 4b. saneamento_basico
            cursor.execute(
                """INSERT INTO saneamento_basico
                (escola_id, IN_AGUA_POTAVEL, IN_AGUA_REDE_PUBLICA, IN_AGUA_POCO_ARTESIANO,
                    IN_AGUA_INEXISTENTE, IN_ENERGIA_REDE_PUBLICA, IN_ENERGIA_INEXISTENTE,
                    IN_ESGOTO_REDE_PUBLICA, IN_ESGOTO_INEXISTENTE, IN_LIXO_SERVICO_COLETA)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    escola_id,
                    bool(row.IN_AGUA_POTAVEL),
                    bool(row.IN_AGUA_REDE_PUBLICA),
                    bool(row.IN_AGUA_POCO_ARTESIANO),
                    bool(row.IN_AGUA_INEXISTENTE),
                    bool(row.IN_ENERGIA_REDE_PUBLICA),
                    bool(row.IN_ENERGIA_INEXISTENTE),
                    bool(row.IN_ESGOTO_REDE_PUBLICA),
                    bool(row.IN_ESGOTO_INEXISTENTE),
                    bool(row.IN_LIXO_SERVICO_COLETA)
                )
            )

            # 4c. infraestrutura
            cursor.execute(
                """INSERT INTO infraestrutura
                (escola_id, IN_ALIMENTACAO, QT_TRANSP_PUBLICO, IN_ALMOXARIFADO, IN_BIBLIOTECA, IN_COZINHA,
                    IN_LABORATORIO_CIENCIAS, IN_LABORATORIO_INFORMATICA,
                    IN_PATIO_COBERTO, IN_PARQUE_INFANTIL, IN_QUADRA_ESPORTES,
                    IN_REFEITORIO, IN_SALA_PROFESSOR)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    escola_id,
                    bool(row.IN_ALIMENTACAO),
                    int(row.QT_TRANSP_PUBLICO),
                    bool(row.IN_ALMOXARIFADO),
                    bool(row.IN_BIBLIOTECA),
                    bool(row.IN_COZINHA),
                    bool(row.IN_LABORATORIO_CIENCIAS),
                    bool(row.IN_LABORATORIO_INFORMATICA),
                    bool(row.IN_PATIO_COBERTO),
                    bool(row.IN_PARQUE_INFANTIL),
                    bool(row.IN_QUADRA_ESPORTES),
                    bool(row.IN_REFEITORIO),
                    bool(row.IN_SALA_PROFESSOR)
                )
            )

            # 4e. corpo_docente
            cursor.execute(
                """INSERT INTO corpo_docente
                (escola_id, QT_PROF_BIBLIOTECARIO, QT_PROF_PEDAGOGIA, QT_PROF_SAUDE,
                    QT_PROF_PSICOLOGO, QT_PROF_ADMINISTRATIVOS, QT_PROF_SERVICOS_GERAIS,
                    QT_PROF_SEGURANCA, QT_PROF_GESTAO, QT_PROF_ASSIST_SOCIAL, QT_PROF_NUTRICIONISTA)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    escola_id,
                    int(row.QT_PROF_BIBLIOTECARIO),
                    int(row.QT_PROF_PEDAGOGIA),
                    int(row.QT_PROF_SAUDE),
                    int(row.QT_PROF_PSICOLOGO),
                    int(row.QT_PROF_ADMINISTRATIVOS),
                    int(row.QT_PROF_SERVICOS_GERAIS),
                    int(row.QT_PROF_SEGURANCA),
                    int(row.QT_PROF_GESTAO),
                    int(row.QT_PROF_ASSIST_SOCIAL),
                    int(row.QT_PROF_NUTRICIONISTA)
                )
            )

            # 4f. matriculas
            cursor.execute(
                """INSERT INTO matriculas
                (escola_id, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_EJA,
                    QT_MAT_ESP, QT_MAT_BAS_FEM, QT_MAT_BAS_MASC, QT_MAT_BAS_BRANCA,
                    QT_MAT_BAS_PRETA, QT_MAT_BAS_PARDA, QT_MAT_BAS_AMARELA,
                    QT_MAT_BAS_INDIGENA)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    escola_id,
                    int(row.QT_MAT_INF),
                    int(row.QT_MAT_FUND),
                    int(row.QT_MAT_MED),
                    int(row.QT_MAT_EJA),
                    int(row.QT_MAT_ESP),
                    int(row.QT_MAT_BAS_FEM),
                    int(row.QT_MAT_BAS_MASC),
                    int(row.QT_MAT_BAS_BRANCA),
                    int(row.QT_MAT_BAS_PRETA),
                    int(row.QT_MAT_BAS_PARDA),
                    int(row.QT_MAT_BAS_AMARELA),
                    int(row.QT_MAT_BAS_INDIGENA)
                )
            )

            # 4g. materiais
            cursor.execute(
                """INSERT INTO materiais
                (escola_id, IN_MATERIAL_PED_CIENTIFICO,
                    IN_MATERIAL_PED_ARTISTICAS, IN_MATERIAL_PED_DESPORTIVA, IN_INTERNET, QT_EQUIP_MULTIMIDIA)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    escola_id,
                    bool(row.IN_MATERIAL_PED_CIENTIFICO),
                    bool(row.IN_MATERIAL_PED_ARTISTICAS),
                    bool(row.IN_MATERIAL_PED_DESPORTIVA),
                    bool(row.IN_INTERNET),
                    int(row.QT_EQUIP_MULTIMIDIA)
                )
            )

        # Grava todas as inserções
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e