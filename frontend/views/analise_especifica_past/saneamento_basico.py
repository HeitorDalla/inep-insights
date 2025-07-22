# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st

# Importando funções utilitárias
from frontend.utils.formatters import bool_to_text
from frontend.utils.graficos import criar_grafico_saneamento

# Função para mostrar a tela de Saneamento Básico
def saneamento_basico(conn, nome_escola_marta, df_escolas, localizacoes_filtradas):
    # Busca dados de saneamento básico da escola de Marta
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

    # Dicionário com as opções de indicadores
    indicadores_opcoes = {
        'Água Potável': ('agua_potavel', False),
        'Água de Rede Pública': ('agua_rede_publica', False),
        'Água de Poço Artesiano': ('agua_poco_artesiano', False),
        'Água Disponível': ('agua_inexistente', True),
        'Esgoto de Rede Pública': ('esgoto_rede_publica', False),
        'Esgoto Disponível': ('esgoto_inexistente', True),
        'Energia de Rede Pública': ('energia_rede_publica', False),
        'Energia Disponível': ('energia_inexistente', True),
        'Coleta de Lixo': ('lixo_servico_coleta', False)
    }

    # Busca dados de saneamento básico das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query baseado no número de escolas
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de todas as escolas filtradas
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
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
            JOIN tipo_localizacao tl 
                ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params = df_escolas["escola_nome"].tolist()

        if localizacoes_filtradas:
            loc_placeholders = ", ".join(["%s"] * len(localizacoes_filtradas))
            sql += f" AND tl.descricao IN ({loc_placeholders})"
            params += localizacoes_filtradas

        escolas_filtradas_df = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_df = pd.DataFrame()

    # Cria layout de duas colunas para títulos
    col1, col2 = st.columns(2)
    
    with col1: 
        st.markdown(f"""
            <h1 class="h1-title-anal_espc">Escola de Marta</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="p-title-anal_espc">{nome_escola_marta}</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <h1 class="h1-title-anal_espc">Escolas Filtradas</h1>
        """, unsafe_allow_html=True)

        if not escolas_filtradas_df.empty:
            qt_escolas_unicas = escolas_filtradas_df["NO_ENTIDADE"].nunique()
            qt_escolas_selecionas_formatted = f'{qt_escolas_unicas:,.0f}'.replace(",", "@").replace(".", ",").replace("@", ".")

            st.markdown(f"""
                <p class="p-title-anal_espc"><b>{qt_escolas_selecionas_formatted}</b> escolas filtradas</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <p class="p-title-anal_espc">Nenhuma escola selecionada</p>
            """, unsafe_allow_html=True)

    # Selectbox para escolher o indicador (com key única)
    indicador_selecionado = st.selectbox(
        "Selecione o indicador:",
        list(indicadores_opcoes.keys()),
        index=0,
        key="saneamento_basico_indicador_selectbox"
    )

    # Obtém o campo e se deve inverter o valor
    campo_selecionado, inverter_inexistente = indicadores_opcoes[indicador_selecionado]

    # Processa os dados da escola de Marta
    if not em_df.empty:
        # Extrai o valor do campo selecionado
        valor_campo = em_df.loc[0, campo_selecionado]
        
        # Aplica inversão se necessário (para campos "inexistente")
        if inverter_inexistente:
            valor_campo = 1 - valor_campo
            
        # Converte para texto
        valor_escola_marta = bool_to_text(valor_campo)
    else:
        # Se não encontrou dados, define como "Não"
        valor_escola_marta = "Não"

    # Cria layout de duas colunas para conteúdo
    
    col3, col4 = st.columns(2)
    # Coluna 1: Dados da escola de Marta
    with col3:
        # KPI único baseado no indicador selecionado
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">{indicador_selecionado}</div>
                <div class="kpi-value anal-espc-kpi-value">{valor_escola_marta}</div>
            </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Gráfico das escolas filtradas
    with col4:
        if not escolas_filtradas_df.empty:
            if not localizacoes_filtradas:
                st.warning("Por favor, selecione ao menos um tipo de localização para visualizar o gráfico.")
            else:
                fig = criar_grafico_saneamento(escolas_filtradas_df, campo_selecionado, indicador_selecionado, inverter_inexistente)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Nenhum dado disponível para os filtros selecionados.")
        else:
            st.warning("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")