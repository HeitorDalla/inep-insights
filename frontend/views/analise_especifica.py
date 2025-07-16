import streamlit as st
import pandas as pd

# Função para mostrar a página de análise específica
def show_analise_especifica_page (conn):
    # SQL Query p/ ler as regiões únicas
    regiao_df = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO 
        FROM regiao 
        ORDER BY NO_REGIAO ASC
        """, conn)
    
    # Selectbox com as regiões únicas
    regiao_selecionada = st.sidebar.selectbox(
        "Selecione a região:",
        options=regiao_df["NO_REGIAO"]
    )

    # SQL Query p/ ler as UFs únicas
    uf_df = pd.read_sql(
        """
        SELECT DISTINCT uf.NO_UF
        FROM uf
        JOIN regiao ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF ASC
        """, conn, params=(regiao_selecionada,)
    )

    # Selectbox com as UFs únicas
    uf_selecionada = st.sidebar.selectbox(
        "Selecione a UF:",
        options=uf_df["NO_UF"]
    )

    # SQL Query p/ ler os municípios únicos
    municipio_df = pd.read_sql(
        """
        SELECT DISTINCT municipio.NO_MUNICIPIO
        FROM municipio
        JOIN uf ON municipio.uf_id = uf.id
        WHERE uf.NO_UF = %s
        ORDER BY municipio.NO_MUNICIPIO ASC
        """, conn, params=(uf_selecionada,)
    )

    # Selectbox com os municípios únicos
    municipio_selecionado = st.sidebar.selectbox(
        "Selecione o município:",
        options=municipio_df["NO_MUNICIPIO"]
    )

    # Multiselect dos tipos de localização (Urbana e Rural)
    tipo_localizacao_df = pd.read_sql("""
        SELECT id, descricao 
        FROM tipo_localizacao 
        ORDER BY descricao ASC
    """, conn)

    tipo_localizacao_list = tipo_localizacao_df["descricao"].tolist()
    tipo_localizacao_selecionada = st.sidebar.multiselect(
        "Selecione o(s) tipo(s) de localização:",
        options=tipo_localizacao_list,
        default=tipo_localizacao_list
    )

    # SQL Query p/ buscar escolas conforme todos os filtros
    # Verifica se o usuário escolheu ao menos um tipo de localização no multiselect. Caso contrário, segue-se para o "else"
    if tipo_localizacao_selecionada:
        # Se o usuário escolheu Urbana e Rural = ["%s"] * 2 = ["%s", "%s"]; e o join resulta em "%s, %s
        placeholders = ", ".join(["%s"] * len(tipo_localizacao_selecionada))

        sql = f"""
            SELECT
                e.id               AS escola_id,
                e.NO_ENTIDADE      AS escola_nome,
                tl.descricao       AS localizacao
            FROM escola e
            JOIN municipio m           ON e.municipio_id       = m.id
            JOIN uf u                  ON m.uf_id              = u.id
            JOIN regiao r              ON u.regiao_id          = r.id
            JOIN tipo_localizacao tl   ON e.tp_localizacao_id  = tl.id
            WHERE r.NO_REGIAO    = %s
            AND u.NO_UF         = %s
            AND m.NO_MUNICIPIO  = %s
            AND tl.descricao    IN ({placeholders})
            ORDER BY e.NO_ENTIDADE ASC
        """
        # SELECT ... AS: renomeia colunas para facilitar o uso

        # JOIN: liga as tabelas escola → município → uf → região e a tabela tipo_localizacao
        
        # WHERE: filtra por região, UF, município e tipo de localização, usando uma lista dinâmica dentro de IN (…)
        
        # ORDER BY: ordena o resultado pelo nome da escola em ordem alfabética

        params = [regiao_selecionada, uf_selecionada, municipio_selecionado] + tipo_localizacao_selecionada
        # Construção da lista de parâmetros que serão passados para o pd.read_sql: Começa com os valores fixos %s correspondentes a Região, UF e Município. Depois concatena a lista de tipos de localização selecionados, para preencher cada %s dentro do IN

        df_escolas = pd.read_sql(sql, conn, params=params)
        # Executa a consulta no banco de dados via Pandas, retornando um DataFrame com as colunas escola_id, escola_nome e localizacao
    else:
        df_escolas = pd.DataFrame(columns=["escola_id", "escola_nome", "localizacao"])
        # Caso não haja nenhum tipo de localização selecionado, cria um DataFrame vazio com as mesmas colunas, evitando erros mais adiante

    # A condição testa se o DataFrame não está vazio
    if not df_escolas.empty:
        # Extrai a coluna de nomes em uma lista de strings, usada no selectbox.
        escolas_nomes = df_escolas["escola_nome"].tolist()

        # Exibe o selectbox na sidebar com todas as escolas encontradas, permitindo ao usuário escolher uma
        escola_selecionada = st.sidebar.selectbox(
            "Selecione a escola:",
            options=escolas_nomes
        )

        # Recupera o id correspondente ao nome escolhido:
        escola_id = int(
            df_escolas.loc[
                df_escolas["escola_nome"] == escola_selecionada,
                "escola_id"
            ].iloc[0]
        )

    else:
        # Se o DataFrame estiver vazio, mostra uma mensagem de alerta e define `escola_selecionada` e `escola_id` como `None`, para que você saiba, no resto do código, que não há seleção válida
        st.sidebar.write("Nenhuma escola encontrada com os filtros selecionados! Por favor, selecione ao menos um tipo de localização.")
        escola_selecionada = None
        escola_id = None

    # Dá estilo às tabs de navegação internas (mover para assets/styles.py)
    st.markdown("""
        <style>
            div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
            }
        </style>
    """,
    unsafe_allow_html=True)

    # Configuração do menu de navegação interno
    tab_saneamento_basico, tab_infraestrutura, tab_material, tab_corpo_docente, tab_matricula = st.tabs([
        "💦 Saneamento Básico",
        "🏫 Infraestrutura",
        "📒 Material",
        "👩🏻 Corpo Docente",
        "🧑🏻‍🎓 Matricula"
    ])

    # Conteúdo da aba "Saneamento Básico"
    with tab_saneamento_basico:
        # Declara uma variável que armazena o nome da escola de Marta (persona). Essa variável será usada como filtro nas consultas ao banco de dados
        nome_escola_marta = "TRABALHO E SABER ESCOLA MUNICIPAL DO CAMPO"

        # Executa uma query SQL e retorna um DataFrame
        em_df = pd.read_sql("""
            SELECT
                sb.IN_AGUA_POTAVEL         AS agua_potavel,
                sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
                sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
                sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
                sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
                sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
                sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
                sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
                sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
            FROM escola e
            JOIN saneamento_basico sb 
                ON sb.escola_id = e.id
            WHERE e.NO_ENTIDADE = %s
        """, conn, params=(nome_escola_marta,))
        # SELECT: seleciona todos os indicadores booleanos de saneamento e renomeia cada coluna para algo mais legível 
        
        # JOIN: liga a tabela "escola" (e) à tabela saneamento_basico (sb) via escola.id

        # WHERE … = %s: filtra apenas pela escola cujo nome é igual ao nome da variável "nome_escola_marta"

        # params=(nome_escola_marta,): passa o nome da variável "nome_escola_marta" como parâmetro para a query SQL

        if escola_selecionada:
        # Se o usuário já tiver escolhido uma escola via sidebar, executa a mesma query acima, mas passando o nome da escola selecionada, e guarda o resultado em outro DataFrame.
            es_df = pd.read_sql("""
                SELECT
                    sb.IN_AGUA_POTAVEL         AS agua_potavel,
                    sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
                    sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
                    sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
                    sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
                    sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
                    sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
                    sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
                    sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
                FROM escola e
                JOIN saneamento_basico sb 
                    ON sb.escola_id = e.id
                WHERE e.NO_ENTIDADE = %s
            """, conn, params=(escola_selecionada,))
        else:
        # Caso contrário, cria um DataFrame vazio com as mesmas colunas, para evitar erros posteriores ao tentar acessar índices inexistentes.
            es_df = pd.DataFrame(columns=[
                "agua_potavel", "agua_rede_publica", "agua_poco_artesiano", "agua_inexistente",
                "esgoto_rede_publica", "esgoto_inexistente",
                "energia_rede_publica", "energia_inexistente",
                "lixo_servico_coleta"
            ])

        # Função auxiliar que recebe um valor 0 ou 1 e devolve 0.0 ou 100.0 respectivamente
        def bool_to_pct(flag: int) -> float:
            # Primeiro converte para bool (0 → False; 1 → True), depois escolhe o percentual correspondente (True → 100.0; False → 0.0)
            return 100.0 if bool(flag) else 0.0

        if not em_df.empty:
        # Verifica se "em_df" não está vazio): se não estiver, extrai cada um dos campos na primeira linha (loc[0, "..."])

        # Para os indicadores de “inexistente” (água, esgoto e energia), inverte-se o valor com (1 - <flag>) para mostrar a disponibilidade

        # Passa tudo pela função "bool_to_pct" para obter 0.0 ou 100.0
            em_agua_potavel_pct        = bool_to_pct(em_df.loc[0, "agua_potavel"])
            em_agua_rede_publica_pct   = bool_to_pct(em_df.loc[0, "agua_rede_publica"])
            em_agua_poco_artesiano_pct = bool_to_pct(em_df.loc[0, "agua_poco_artesiano"])
            em_agua_inexistente_pct    = bool_to_pct(1 - em_df.loc[0, "agua_inexistente"])
            em_esgoto_rede_publica_pct = bool_to_pct(em_df.loc[0, "esgoto_rede_publica"])
            em_esgoto_inexistente_pct  = bool_to_pct(1 - em_df.loc[0, "esgoto_inexistente"])
            em_energia_rede_publica_pct= bool_to_pct(em_df.loc[0, "energia_rede_publica"])
            em_energia_inexistente_pct = bool_to_pct(1 - em_df.loc[0, "energia_inexistente"])
            em_lixo_servico_coleta_pct = bool_to_pct(em_df.loc[0, "lixo_servico_coleta"])
        else:
        # Se "em_df" estiver vazio, atribui 0.0 a todas as variáveis de percentuais de Marta
            em_agua_potavel_pct = em_agua_rede_publica_pct = em_agua_poco_artesiano_pct = 0.0
            em_agua_inexistente_pct = em_esgoto_rede_publica_pct = em_esgoto_inexistente_pct = 0.0
            em_energia_rede_publica_pct = em_energia_inexistente_pct = em_lixo_servico_coleta_pct = 0.0
        
        # Idêntico ao bloco anterior, mas para a escola selecionada
        if not es_df.empty:
            es_agua_potavel_pct        = bool_to_pct(es_df.loc[0, "agua_potavel"])
            es_agua_rede_publica_pct   = bool_to_pct(es_df.loc[0, "agua_rede_publica"])
            es_agua_poco_artesiano_pct = bool_to_pct(es_df.loc[0, "agua_poco_artesiano"])
            es_agua_inexistente_pct    = bool_to_pct(1 - es_df.loc[0, "agua_inexistente"])
            es_esgoto_rede_publica_pct = bool_to_pct(es_df.loc[0, "esgoto_rede_publica"])
            es_esgoto_inexistente_pct  = bool_to_pct(1 - es_df.loc[0, "esgoto_inexistente"])
            es_energia_rede_publica_pct= bool_to_pct(es_df.loc[0, "energia_rede_publica"])
            es_energia_inexistente_pct = bool_to_pct(1 - es_df.loc[0, "energia_inexistente"])
            es_lixo_servico_coleta_pct = bool_to_pct(es_df.loc[0, "lixo_servico_coleta"])
        else:
            es_agua_potavel_pct = es_agua_rede_publica_pct = es_agua_poco_artesiano_pct = 0.0
            es_agua_inexistente_pct = es_esgoto_rede_publica_pct = es_esgoto_inexistente_pct = 0.0
            es_energia_rede_publica_pct = es_energia_inexistente_pct = es_lixo_servico_coleta_pct = 0.0

        # Cria um layout de duas colunas iguais no Streamlit, atribuídas às variáveis col1 (esquerda) e col2 (direita)
        col1, col2 = st.columns(2)

        # Injeta CSS p/ centralizar <h1/> e <p/> (mover para assets/style.py)
        st.markdown("""
            <style>
                h1, p {
                    text-align: center;
                }       
            </style>
        """, unsafe_allow_html=True)

        # st.metric: para cada indicador, exibe um cartão com rótulo e valor formatado (:.0f)
        with col1:
            st.markdown("""
                <h1>Escola de Marta</h1>
            """,
            unsafe_allow_html=True)
            st.markdown(f"""
                <p>{nome_escola_marta}</p>
            """,
            unsafe_allow_html=True)
            st.metric("Água Potável",             f"{em_agua_potavel_pct:.0f}%", border=True)
            st.metric("Água Rede Pública",        f"{em_agua_rede_publica_pct:.0f}%", border=True)
            st.metric("Poço Artesiano",           f"{em_agua_poco_artesiano_pct:.0f}%", border=True)
            st.metric("Esgoto Disponível",        f"{em_esgoto_inexistente_pct:.0f}%", border=True)
            st.metric("Esgoto Rede Pública",      f"{em_esgoto_rede_publica_pct:.0f}%", border=True)
            st.metric("Energia Disponível",       f"{em_energia_inexistente_pct:.0f}%", border=True)
            st.metric("Energia Rede Pública",     f"{em_energia_rede_publica_pct:.0f}%", border=True)
            st.metric("Coleta de Lixo",           f"{em_lixo_servico_coleta_pct:.0f}%", border=True)

        with col2:
            st.markdown("""
                <h1>Escola selecionada</h1>
            """,
            unsafe_allow_html=True)
            st.markdown(f"""
                <p>{escola_selecionada}</p>
            """,
            unsafe_allow_html=True)
            if escola_selecionada:
                st.metric("Água Potável",         f"{es_agua_potavel_pct:.0f}%", border=True)
                st.metric("Água Rede Pública",    f"{es_agua_rede_publica_pct:.0f}%", border=True)
                st.metric("Poço Artesiano",       f"{es_agua_poco_artesiano_pct:.0f}%", border=True)
                st.metric("Esgoto Disponível",    f"{es_esgoto_inexistente_pct:.0f}%", border=True)
                st.metric("Esgoto Rede Pública",  f"{es_esgoto_rede_publica_pct:.0f}%", border=True)
                st.metric("Energia Disponível",   f"{es_energia_inexistente_pct:.0f}%", border=True)
                st.metric("Energia Rede Pública", f"{es_energia_rede_publica_pct:.0f}%", border=True)
                st.metric("Coleta de Lixo",       f"{es_lixo_servico_coleta_pct:.0f}%", border=True)
            else:
                st.write("Por favor, selecione uma escola válida.")

    # Conteúdo da aba "Infraestrutura"
    with tab_infraestrutura:
        st.header("Infraestrutura")

    # Conteúdo da aba "Material"
    with tab_material:
        st.header("Material")

    # Conteúdo da aba "Corpo Docente"
    with tab_corpo_docente:
        st.header("Corpo Docente")

    # Conteúdo da aba "Matrícula"
    with tab_matricula:
        st.header("Matrícula")