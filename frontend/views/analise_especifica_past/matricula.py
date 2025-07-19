# frontend/views/analise_especifica_past/matricula.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def matricula(conn, nome_escola_marta, df_escolas):
    pass
    # st.title("📊 Análise Completa de Matrículas")
    
    # # =============================================
    # # 1. INTRODUÇÃO E CONTEXTO
    # # =============================================
    # st.markdown("""
    # <div style="background-color:#f8f9fa;padding:20px;border-radius:10px;border-left:5px solid #4e73df;margin-bottom:30px;">
    #     <h3 style="color:#2c3e50;margin-top:0;">📌 Contexto Estratégico</h3>
    #     <p style="color:#34495e;font-size:16px;">
    #     Esta análise combina <b>visualizações detalhadas</b> com <b>insights acionáveis</b> para embasar suas decisões como gestora escolar. 
    #     Compare sua escola com outras da região e identifique oportunidades de melhoria.
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)

    # # =============================================
    # # 2. DADOS DA ESCOLA DA MARTA (DESTAQUE)
    # # =============================================
    # st.header("🏫 Perfil da Sua Escola", divider='blue')
    
    # # Query para dados da Marta
    # query_marta = """
    # SELECT 
    #     QT_MAT_INF as Infantil,
    #     QT_MAT_FUND as Fundamental,
    #     QT_MAT_MED as Médio,
    #     QT_MAT_EJA as EJA,
    #     QT_MAT_ESP as Especial,
    #     QT_MAT_BAS_FEM as Feminino,
    #     QT_MAT_BAS_MASC as Masculino,
    #     (QT_MAT_BAS_PRETA + QT_MAT_BAS_PARDA) as Pretos_Pardos,
    #     QT_MAT_BAS_BRANCA as Branca,
    #     QT_MAT_BAS_INDIGENA as Indígena
    # FROM matriculas m
    # JOIN escola e ON m.escola_id = e.id
    # WHERE e.NO_ENTIDADE = %s
    # """
    # df_marta = pd.read_sql(query_marta, conn, params=(nome_escola_marta,))

    # if not df_marta.empty:
    #     total_alunos = df_marta.iloc[0].sum()
        
    #     # Layout de colunas para métricas
    #     col1, col2, col3 = st.columns(3)
    #     with col1:
    #         st.metric("👥 Total de Alunos", total_alunos)
    #     with col2:
    #         percent_eja = (df_marta['EJA'].iloc[0]/total_alunos)*100 if total_alunos > 0 else 0
    #         st.metric("👩‍🎓 Educação de Jovens/Adultos", f"{percent_eja:.1f}%")
    #     with col3:
    #         percent_pp = (df_marta['Pretos_Pardos'].iloc[0]/total_alunos)*100 if total_alunos > 0 else 0
    #         st.metric("✊🏽 Pretos/Pardos", f"{percent_pp:.1f}%")

    #     # Gráfico 1: Composição por Nível Educacional
    #     fig_nivel = px.pie(
    #         df_marta.melt(value_vars=['Infantil', 'Fundamental', 'Médio', 'EJA', 'Especial']),
    #         names='variable',
    #         values='value',
    #         title='<b>Distribuição por Nível Educacional</b>',
    #         hole=0.4,
    #         color_discrete_sequence=px.colors.sequential.Blues_r
    #     )
    #     fig_nivel.update_traces(textposition='inside', textinfo='percent+label')
    #     st.plotly_chart(fig_nivel, use_container_width=True)
        
    #     st.markdown("""
    #     <div style="background-color:#e8f4f8;padding:15px;border-radius:10px;margin-top:-10px;">
    #         <h4 style="color:#2980b9;margin-top:0;">📝 Interpretação:</h4>
    #         <ul style="color:#2c3e50;">
    #             <li>A maior concentração está no <b>{}</b>, representando {:.1f}% do total</li>
    #             <li>O EJA (Educação de Jovens/Adultos) corresponde a <b>{:.1f}%</b> - {} que a média regional</li>
    #             <li>{} alunos com necessidades especiais atendidos</li>
    #         </ul>
    #     </div>
    #     """.format(
    #         df_marta[['Infantil', 'Fundamental', 'Médio']].iloc[0].idxmax(),
    #         (df_marta[['Infantil', 'Fundamental', 'Médio']].iloc[0].max()/total_alunos)*100,
    #         percent_eja,
    #         "Acima" if percent_eja > 15 else "Abaixo",
    #         df_marta['Especial'].iloc[0]
    #     ), unsafe_allow_html=True)

    #     # Gráfico 2: Perfil Demográfico
    #     fig_demo = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
        
    #     # Subplot 1: Gênero
    #     fig_demo.add_trace(go.Pie(
    #         labels=['Feminino', 'Masculino'],
    #         values=[df_marta['Feminino'].iloc[0], df_marta['Masculino'].iloc[0]],
    #         name="Gênero",
    #         marker_colors=['#ff9999','#66b3ff'],
    #         hole=0.5
    #     ), 1, 1)
        
    #     # Subplot 2: Raça/Cor
    #     raca_values = [
    #         df_marta['Branca'].iloc[0],
    #         df_marta['Pretos_Pardos'].iloc[0],
    #         df_marta['Indígena'].iloc[0]
    #     ]
    #     fig_demo.add_trace(go.Pie(
    #         labels=['Branca', 'Preta/Parda', 'Indígena'],
    #         values=raca_values,
    #         name="Raça/Cor",
    #         marker_colors=['#f6c23e','#1cc88a','#e74a3b'],
    #         hole=0.5
    #     ), 1, 2)
        
    #     fig_demo.update_layout(
    #         title_text="<b>Perfil Demográfico dos Alunos</b>",
    #         annotations=[
    #             dict(text='Gênero', x=0.18, y=0.5, font_size=14, showarrow=False),
    #             dict(text='Raça/Cor', x=0.82, y=0.5, font_size=14, showarrow=False)
    #         ]
    #     )
    #     st.plotly_chart(fig_demo, use_container_width=True)
        
    #     st.markdown("""
    #     <div style="background-color:#fff8e1;padding:15px;border-radius:10px;margin-top:-10px;">
    #         <h4 style="color:#e65100;margin-top:0;">🌍 Diversidade:</h4>
    #         <ul style="color:#2c3e50;">
    #             <li><b>{:.1f}%</b> dos alunos se declaram pretos ou pardos</li>
    #             <li><b>{} aluno(s)</b> indígena(s) - {} atendimento especializado</li>
    #             <li>Proporção de gêneros: <b>{:.1f}% feminino</b> vs <b>{:.1f}% masculino</b></li>
    #         </ul>
    #     </div>
    #     """.format(
    #         percent_pp,
    #         df_marta['Indígena'].iloc[0],
    #         "Requer" if df_marta['Indígena'].iloc[0] > 0 else "Não requer",
    #         (df_marta['Feminino'].iloc[0]/total_alunos)*100,
    #         (df_marta['Masculino'].iloc[0]/total_alunos)*100
    #     ), unsafe_allow_html=True)

    # else:
    #     st.warning("Dados não encontrados para a escola de referência.")

    # # =============================================
    # # 3. COMPARAÇÃO COM OUTRAS ESCOLAS
    # # =============================================
    # if not df_escolas.empty:
    #     st.header("🆚 Comparativo Regional", divider='blue')
        
    #     # Query para escolas filtradas
    #     escola_ids = ','.join([str(id) for id in df_escolas['escola_id']])
    #     query_comp = f"""
    #     SELECT 
    #         e.NO_ENTIDADE as escola_nome,
    #         tl.descricao as localizacao,
    #         m.QT_MAT_INF as Infantil,
    #         m.QT_MAT_FUND as Fundamental,
    #         m.QT_MAT_MED as Médio,
    #         m.QT_MAT_EJA as EJA,
    #         m.QT_MAT_ESP as Especial,
    #         (m.QT_MAT_BAS_PRETA + m.QT_MAT_BAS_PARDA) as Pretos_Pardos,
    #         m.QT_MAT_BAS_FEM as Feminino
    #     FROM matriculas m
    #     JOIN escola e ON m.escola_id = e.id
    #     JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    #     WHERE m.escola_id IN ({escola_ids})
    #     """
    #     df_comparativo = pd.read_sql(query_comp, conn)
        
    #     if not df_comparativo.empty:
    #         # Adiciona escola da Marta ao comparativo
    #         if not df_marta.empty:
    #             marta_row = pd.DataFrame({
    #                 'escola_nome': [nome_escola_marta],
    #                 'localizacao': ['Sua Escola'],
    #                 'Infantil': [df_marta['Infantil'].iloc[0]],
    #                 'Fundamental': [df_marta['Fundamental'].iloc[0]],
    #                 'Médio': [df_marta['Médio'].iloc[0]],
    #                 'EJA': [df_marta['EJA'].iloc[0]],
    #                 'Especial': [df_marta['Especial'].iloc[0]],
    #                 'Pretos_Pardos': [df_marta['Pretos_Pardos'].iloc[0]],
    #                 'Feminino': [df_marta['Feminino'].iloc[0]]
    #             })
    #             df_comparativo = pd.concat([df_comparativo, marta_row])
            
    #         # Gráfico 3: Comparativo de Níveis Educacionais
    #         st.subheader("📚 Distribuição por Nível de Ensino")
            
    #         fig_comp_nivel = px.bar(
    #             df_comparativo.melt(id_vars=['escola_nome', 'localizacao'], 
    #                               value_vars=['Infantil', 'Fundamental', 'Médio', 'EJA', 'Especial']),
    #             x='escola_nome',
    #             y='value',
    #             color='variable',
    #             facet_row='localizacao',
    #             labels={'value':'Número de Matrículas', 'escola_nome':'Escola'},
    #             color_discrete_sequence=px.colors.qualitative.Pastel,
    #             height=600
    #         )
    #         fig_comp_nivel.update_layout(
    #             title='<b>Comparativo Detalhado por Nível Educacional</b>',
    #             hovermode='x unified'
    #         )
    #         st.plotly_chart(fig_comp_nivel, use_container_width=True)
            
    #         # Análise comparativa
    #         st.markdown("""
    #             <div style="background-color:#e8f5e9;padding:15px;border-radius:10px;margin-top:-10px;">
    #                 <h4 style="color:#2e7d32;margin-top:0;">🔍 Insights Comparativos:</h4>
    #                 <ul style="color:#2c3e50;">
    #                     <li>Sua escola está no <b>{:.0f}º lugar</b> em tamanho total entre {} escolas</li>
    #                     <li>O EJA representa <b>{:.1f}%</b> do total (média regional: {:.1f}%)</li>
    #                     <li><b>{}</b> que a média em atendimento a alunos especiais</li>
    #                 </ul>
    #             </div>
    #             """.format(
    #                 df_comparativo[['Infantil','Fundamental','Médio','EJA','Especial']]
    #                 .sum(axis=1)
    #                 .rank(ascending=False)
    #                 [df_comparativo['escola_nome'] == nome_escola_marta].values[0],  # 1º argumento: posição no ranking
    #                 len(df_comparativo),  # 2º argumento: total de escolas
    #                 percent_eja,  # 3º argumento: % EJA na escola da Marta
    #                 (df_comparativo['EJA'].mean() / df_comparativo[['Infantil','Fundamental','Médio','EJA','Especial']].sum(axis=1).mean()) * 100,  # 4º argumento: % EJA médio regional
    #                 "Acima" if df_marta['Especial'].iloc[0] > df_comparativo['Especial'].mean() else "Abaixo"  # 5º argumento: comparação de alunos especiais
    #             ), unsafe_allow_html=True)

    #         # Gráfico 4: Mapa de Calor de Correlação
    #         st.subheader("🔗 Relações entre Variáveis")
            
    #         correlacao = df_comparativo[['Infantil','Fundamental','Médio','EJA','Especial','Pretos_Pardos','Feminino']].corr()
            
    #         fig_heatmap = px.imshow(
    #             correlacao,
    #             text_auto='.2f',
    #             color_continuous_scale='RdBu',
    #             aspect='auto',
    #             labels=dict(x="Variável", y="Variável", color="Correlação"),
    #             title='<b>Mapa de Correlação entre Indicadores</b>'
    #         )
    #         st.plotly_chart(fig_heatmap, use_container_width=True)
            
    #         st.markdown("""
    #         <div style="background-color:#f3e5f5;padding:15px;border-radius:10px;margin-top:-10px;">
    #             <h4 style="color:#9c27b0;margin-top:0;">📊 Padrões Identificados:</h4>
    #             <ul style="color:#2c3e50;">
    #                 <li>Relação <b>{}</b> entre EJA e matrículas no Fundamental</li>
    #                 <li>Correlação <b>{}</b> entre alunos especiais e infraestrutura</li>
    #                 <li>Distribuição <b>{}</b> por gênero entre os níveis educacionais</li>
    #             </ul>
    #         </div>
    #         """.format(
    #             "positiva" if correlacao.loc['EJA','Fundamental'] > 0 else "negativa",
    #             "forte" if abs(correlacao.loc['Especial','Infantil']) > 0.3 else "fraca",
    #             "equilibrada" if abs(correlacao.loc['Feminino','Médio'] - 0.5) < 0.2 else "desigual"
    #         ), unsafe_allow_html=True)

    # # =============================================
    # # 4. RECOMENDAÇÕES ESTRATÉGICAS
    # # =============================================
    # st.header("🚀 Recomendações para Gestão", divider='blue')
    
    # with st.expander("📈 Prioridades de Ação Baseadas nos Dados", expanded=True):
    #     st.markdown("""
    #     <div style="background-color:#fff3e0;padding:20px;border-radius:10px;">
    #         <h4 style="color:#e65100;margin-top:0;">🎯 Foco Imediato:</h4>
    #         <ol style="color:#2c3e50;font-size:16px;">
    #             <li><b>Ampliar o EJA</b> - {} alunos atendidos ({}% do total)</li>
    #             <li><b>Capacitar professores</b> para educação especial - {} alunos com necessidades específicas</li>
    #             <li><b>Programas de equidade</b> - {}% de alunos pretos/pardos</li>
    #         </ol>
            
    #         <h4 style="color:#e65100;margin-top:20px;">📅 Planejamento de Longo Prazo:</h4>
    #         <ul style="color:#2c3e50;font-size:16px;">
    #             <li>Analisar a <b>evasão escolar</b> por nível educacional</li>
    #             <li>Mapear <b>necessidades de infraestrutura</b> por perfil de alunos</li>
    #             <li>Criar <b>indicadores personalizados</b> de desempenho</li>
    #         </ul>
    #     </div>
    #     """.format(
    #         df_marta['EJA'].iloc[0] if not df_marta.empty else "N/D",
    #         percent_eja if not df_marta.empty else "N/D",
    #         df_marta['Especial'].iloc[0] if not df_marta.empty else "N/D",
    #         percent_pp if not df_marta.empty else "N/D"
    #     ), unsafe_allow_html=True)

    
    # if not df_escolas.empty and not df_comparativo.empty:
    #     with st.expander("💡 Como Usar Esses Dados em Solicitações"):
    #         st.markdown("""
    #         <div style="background-color:#e3f2fd;padding:20px;border-radius:10px;">
    #             <h4 style="color:#1565c0;margin-top:0;">📝 Argumentos para Secretarias:</h4>
    #             <ul style="color:#2c3e50;font-size:16px;">
    #                 <li><i>"Nosso EJA atende {} alunos ({:.1f}% do total), acima da média regional de {:.1f}%"</i></li>
    #                 <li><i>"Necessitamos de recursos para educação especial, com {} alunos atendidos"</i></li>
    #                 <li><i>"{:.1f}% dos nossos alunos são pretos/pardos, demandando políticas afirmativas"</i></li>
    #             </ul>
                
    #             <h4 style="color:#1565c0;margin-top:20px;">🤝 Dados para Parcerias:</h4>
    #             <ul style="color:#2c3e50;font-size:16px;">
    #                 <li>Empresas: <i>"X% dos nossos alunos são do EJA - potencial para programas de qualificação"</i></li>
    #                 <li>ONGs: <i>"Y alunos indígenas necessitam de apoio cultural específico"</i></li>
    #             </ul>
    #         </div>
    #         """.format(
    #             df_marta['EJA'].iloc[0] if not df_marta.empty else 0,
    #             percent_eja if not df_marta.empty else 0,
    #             (df_comparativo['EJA'].mean()/df_comparativo[['Infantil','Fundamental','Médio','EJA','Especial']].sum(axis=1).mean())*100 if not df_comparativo.empty else 0,
    #             df_marta['Especial'].iloc[0] if not df_marta.empty else 0,
    #             percent_pp if not df_marta.empty else 0
    #         ), unsafe_allow_html=True)  