# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Função para carregar os estilos CSS
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Função para mostrar a tela de Saneamento Básico
def saneamento_basico(conn, nome_escola_marta, df_escolas):
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

    # Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
    def bool_to_text(flag: int) -> str:
        return "Sim" if bool(flag) else "Não"

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

    # Selectbox para escolher o indicador
    indicador_selecionado = st.selectbox(
        "Selecione o indicador de saneamento:",
        list(indicadores_opcoes.keys()),
        index=0
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
        escolas_filtradas_df = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_df = pd.DataFrame()

    # Cria layout de duas colunas
    col1, col2 = st.columns(2)

    # Define função para criar gráfico
    def criar_grafico(dados_df, campo, titulo, inverter_inexistente=False):
        if not dados_df.empty:
            # Calcula porcentagem por tipo de localização
            if inverter_inexistente:
                # Para campos "inexistente", inverte o valor (1 - valor)
                dados_agrupados = dados_df.groupby('localizacao')[campo].apply(
                    lambda x: (1 - x).mean() * 100
                ).reset_index()
            else:
                # Para outros campos, calcula média normal
                dados_agrupados = dados_df.groupby('localizacao')[campo].mean().reset_index()
                dados_agrupados[campo] = dados_agrupados[campo] * 100
            
            # Cria gráfico de barras
            fig = px.bar(
                dados_agrupados,
                x='localizacao',
                y=campo,
                title=f'{titulo} (%)',
                labels={'localizacao': 'Localização', campo: 'Porcentagem (%)'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            # Ajusta layout do gráfico com estilo personalizado
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': f'{titulo} (%)',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 20,
                        'color': '#4a4a4a'
                    }
                },
                
                # Estiliza os eixos
                xaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                yaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                )
            )
            
            # Adiciona valores no topo das barras
            fig.update_traces(
                texttemplate='%{y:.1f}%', 
                textposition='inside',
                textfont=dict(size=18, color='white')
            )
            
            return fig
        return None

    # Coluna 1: Dados da escola de Marta
    with col1:
        st.markdown(f"""
            <h1 class="h1-title-anal_espc">Escola de Marta</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="p-title-anal_espc">{nome_escola_marta}</p>
        """, unsafe_allow_html=True)

        # KPI único baseado no indicador selecionado
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">{indicador_selecionado}</div>
                <div class="kpi-value anal-espc-kpi-value">{valor_escola_marta}</div>
            </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Gráfico das escolas filtradas
    with col2:
        st.markdown(f"""
            <h1 class="h1-title-anal_espc">Escolas Filtradas</h1>
        """, unsafe_allow_html=True)
        
        if not escolas_filtradas_df.empty:
            qt_escolas_selecionas = f"{len(escolas_filtradas_df):,.0f}"
            qt_escolas_selecionas_formatted = qt_escolas_selecionas.replace(",", "@").replace(".", ",").replace("@", ".")

            st.markdown(f"""
                <p class="p-title-anal_espc"><b>{qt_escolas_selecionas_formatted}</b> escolas filtradas</p>
            """, unsafe_allow_html=True)

            # Cria gráfico para o indicador selecionado
            fig = criar_grafico(escolas_filtradas_df, campo_selecionado, indicador_selecionado, inverter_inexistente)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            # Se não há escolas filtradas, exibe mensagem informativa
            st.markdown("""
                <p class="p-title-anal_espc">Nenhuma escola selecionada</p>
            """, unsafe_allow_html=True)
            
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")