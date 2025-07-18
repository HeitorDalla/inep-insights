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

# Função para mostrar a tela de materiais pedagógicos
def material(conn, nome_escola_marta, df_escolas):
    # Busca dados de materiais da escola de Marta
    em_mat = pd.read_sql(
        """
        SELECT
            m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
            m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
            m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
            m.IN_INTERNET AS internet,
            m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
        FROM escola e
        JOIN materiais m
            ON m.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)
    )

    # Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
    def bool_to_text(flag: int) -> str:
        return "Sim" if bool(flag) else "Não"

    # Processa os dados da escola de Marta
    if not em_mat.empty:
        with st.expander("ⓘ Com dúvidas? Clique para abrir o glossário"):
            st.markdown("""
            1. **Material Científico** ─ Instrumentos e materiais socioculturais e/ou pedagógicos em uso na escola para o desenvolvimento de atividades de ensino e aprendizagem ─ Conjunto de materiais científicos;
            2. **Material Artístico** ─ Instrumentos e materiais socioculturais e/ou pedagógicos em uso na escola para o desenvolvimento de atividades de ensino e aprendizagem - Materiais para atividades culturais e artísticas;
            3. **Material Esportivo** ─ Instrumentos e materiais socioculturais e/ou pedagógicos em uso na escola para o desenvolvimento de atividades de ensino e aprendizagem - Materiais para prática desportiva e recreação;
            4. **Internet** ─ Acesso à Internet;
            5. **Equipamentos de Multimídia** ─ Quantidade de Projetores Multimídia (Datashow).
            """)

        # Extrai os valores da primeira linha e converte para texto
        em_vals = {
            'material_cientifico': bool_to_text(em_mat.loc[0, 'material_cientifico']),
            'material_artistico': bool_to_text(em_mat.loc[0, 'material_artistico']),
            'material_esportivo': bool_to_text(em_mat.loc[0, 'material_esportivo']),
            'internet': bool_to_text(em_mat.loc[0, 'internet']),
            'equipamentos_multimidia': int(em_mat.loc[0, 'equipamentos_multimidia'])
        }
    else:
        # Se não encontrou dados, define todos como "Não" ou 0
        em_vals = {
            'material_cientifico': "Não",
            'material_artistico': "Não",
            'material_esportivo': "Não",
            'internet': "Não",
            'equipamentos_multimidia': 0
        }

    # Busca dados de materiais das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query baseado no número de escolas
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de todas as escolas filtradas
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
                m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
                m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
                m.IN_INTERNET AS internet,
                m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
            FROM escola e
            JOIN materiais m ON m.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_mat = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_mat = pd.DataFrame()

    # Cria layout de duas colunas
    col1, col2 = st.columns(2)

    # Coluna 1: Dados da escola de Marta
    with col1:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escola de Marta</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="p-title-anal_espc">{nome_escola_marta}</p>
        """, unsafe_allow_html=True)

        # KPI 1: Material Científico
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">Material Científico</div>
                <div class="kpi-value anal-espc-kpi-value">{em_vals['material_cientifico']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # KPI 2: Material Artístico
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">Material Artístico</div>
                <div class="kpi-value anal-espc-kpi-value">{em_vals['material_artistico']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # KPI 3: Material Esportivo
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">Material Esportivo</div>
                <div class="kpi-value anal-espc-kpi-value">{em_vals['material_esportivo']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # KPI 4: Internet
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">Internet</div>
                <div class="kpi-value anal-espc-kpi-value">{em_vals['internet']}</div>
            </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Gráficos das escolas filtradas
    with col2:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escolas Filtradas</h1>
        """, unsafe_allow_html=True)
        
        if not escolas_filtradas_mat.empty:
            qt_escolas_selecionadas = f"{len(escolas_filtradas_mat):,.0f}"
            qt_escolas_selecionadas_formatted = qt_escolas_selecionadas.replace(",", "@").replace(".", ",").replace("@", ".")

            st.markdown(f"""
                <p class="p-title-anal_espc"><b>{qt_escolas_selecionadas_formatted}</b> escolas filtradas</p>
            """, unsafe_allow_html=True)
            
            # Define função para criar gráfico de materiais
            def criar_grafico_material(dados_df, campo, titulo):
                if not dados_df.empty:
                    # Calcula porcentagem por tipo de localização
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
                            title_font=dict(size=12, color='#4a4a4a'),
                            range=[0, 100]
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
            
            # Lista dos indicadores de materiais para criar gráficos
            indicadores_materiais = [
                ('material_cientifico', 'Material Científico'),
                ('material_artistico', 'Material Artístico'),
                ('material_esportivo', 'Material Esportivo'),
                ('internet', 'Internet')
            ]
            
            # Para cada indicador de material, cria um gráfico
            for campo, titulo in indicadores_materiais:
                fig = criar_grafico_material(escolas_filtradas_mat, campo, titulo)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

        else:
            # Se não há escolas filtradas, exibe mensagem informativa
            st.markdown("""
                <p class="p-title-anal_espc">Nenhuma escola selecionada</p>
            """, unsafe_allow_html=True)
            
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")
    
    # Seção de análise de equipamentos multimídia - fora das colunas
    if not escolas_filtradas_mat.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # KPI 5: Quantidade de Equipamentos Multimídia
        equipamentos_formatted = f"{em_vals['equipamentos_multimidia']:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Quantidade de Equipamentos Multimídia (EM) da Escola de Marta</div>
                <div class="kpi-value">{equipamentos_formatted}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Divide em 2 colunas para os gráficos de equipamentos multimídia
        col_eq1, col_eq2 = st.columns(2)
        
        with col_eq1:
            # Gráfico de barras - Média por localização
            equipamentos_stats = escolas_filtradas_mat.groupby('localizacao')['equipamentos_multimidia'].mean().reset_index()
            
            fig_media = px.bar(
                equipamentos_stats,
                x='localizacao',
                y='equipamentos_multimidia',
                title='Média de EM das Escolas Filtradas',
                labels={'localizacao': 'Localização', 'equipamentos_multimidia': 'Quantidade Média'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            fig_media.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': 'Média de EM das Escolas Filtradas',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 16,
                        'color': '#4a4a4a'
                    }
                },
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
            
            fig_media.update_traces(
                texttemplate='%{y:.1f}', 
                textposition='inside',
                textfont=dict(size=14, color='white')
            )
            
            st.plotly_chart(fig_media, use_container_width=True)
        
        with col_eq2:
            # Box Plot - Distribuição por localização
            fig_box = px.box(
                escolas_filtradas_mat,
                x='localizacao',
                y='equipamentos_multimidia',
                title='Distribuição de EM das Escolas Filtradas',
                labels={'localizacao': 'Localização', 'equipamentos_multimidia': 'Quantidade'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            fig_box.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': 'Distribuição de EM das Escolas Filtradas',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 16,
                        'color': '#4a4a4a'
                    }
                },
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
            
            st.plotly_chart(fig_box, use_container_width=True)
        
    elif not df_escolas.empty:
        st.markdown("""
            <h2 style='color: #4a4a4a; margin-top: 40px;'>📊 Análise de Equipamentos Multimídia</h2>
        """, unsafe_allow_html=True)
        
        st.info("Dados de equipamentos multimídia não disponíveis para as escolas filtradas.")