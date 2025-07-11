import pandas as pd

colunas_uteis = [
    # Identificação e Contexto Geográfica
    'NO_REGIAO',  # Nome da região geográfica (Norte, Nordeste, etc.)
    'NO_UF',  # Nome da Unidade Federativa (estado)
    'NO_MUNICIPIO',  # Nome do município onde a escola está localizada
    'TP_LOCALIZACAO',  # Tipo de localização (1-Urbana, 2-Rural)
    'TP_LOCALIZACAO_DIFERENCIADA',  # Localização em áreas específicas (1-Área de assentamento, 2-Terra indígena, etc.)
    'TP_SITUACAO_FUNCIONAMENTO',  # Situação de funcionamento (1-Em atividade, 2-Paralisada, etc.)
    'TP_DEPENDENCIA',  # Dependência administrativa (1-Federal, 2-Estadual, 3-Municipal, 4-Privada)

    # Infraestrutura Básica
    'IN_AGUA_POTAVEL',  # Possui água potável (Sim/Não)
    'IN_AGUA_INEXISTENTE',  # Não possui água (Sim/Não)
    'IN_AGUA_POCO_ARTESIANO',  # Utiliza poço artesiano (Sim/Não)    
    'IN_AGUA_REDE_PUBLICA',  # Água proveniente de rede pública (Sim/Não)
    'IN_ESGOTO_INEXISTENTE',  # Não possui sistema de esgoto (Sim/Não)
    'IN_ENERGIA_INEXISTENTE',  # Não possui energia elétrica (Sim/Não)
    'IN_LIXO_SERVICO_COLETA',  # Lixo coletado por serviço de limpeza (Sim/Não)
    'IN_ENERGIA_REDE_PUBLICA',  # Energia da rede pública (Sim/Não)
    'IN_ESGOTO_REDE_PUBLICA',  # Esgoto por rede pública (Sim/Não)

    # Espaços pedagógicos
    'IN_PATIO_COBERTO',  # Possui pátio coberto (Sim/Não)
    'IN_BIBLIOTECA',  # Possui biblioteca (Sim/Não)
    'IN_LABORATORIO_CIENCIAS',  # Possui laboratório de ciências (Sim/Não)
    'IN_LABORATORIO_INFORMATICA',  # Possui laboratório de informática (Sim/Não)
    'IN_QUADRA_ESPORTES',  # Possui quadra de esportes (Sim/Não)
    'IN_PARQUE_INFANTIL',  # Possui parque infantil (Sim/Não)
    'IN_SALA_PROFESSOR',  # Possui sala dos professores (Sim/Não)
    'IN_COZINHA',  # Possui cozinha (Sim/Não)
    'IN_REFEITORIO',  # Possui refeitório (Sim/Não)
    'IN_ALMOXARIFADO',  # Possui almoxarifado (Sim/Não)

    # Conectividade
    'IN_INTERNET',  # Possui acesso à internet (Sim/Não)
    'IN_EQUIP_TV',  # Possui televisores (Sim/Não)
    'QT_EQUIP_MULTIMIDIA',
    'QT_DESKTOP_ALUNO',
    'QT_TABLET_ALUNO',

    # Recursos humanos (qualificação do ensino)
    'QT_PROF_BIBLIOTECARIO',
    'QT_PROF_PEDAGOGIA',
    'QT_PROF_SAUDE',
    'QT_PROF_PSICOLOGO',
    'QT_PROF_ADMINISTRATIVOS',
    'QT_PROF_SERVICOS_GERAIS',
    'QT_PROF_SEGURANCA',
    'QT_PROF_GESTAO',
    'QT_PROF_ASSIST_SOCIAL',
    'QT_PROF_NUTRICIONISTA',

    # Mátriculas
    'QT_MAT_INF', # Educação Infantil
    'QT_MAT_FUND', # Fundamental
    'QT_MAT_MED', # Ensino Médio
    'QT_MAT_EJA', # EJA
    'QT_MAT_ESP', # Educação Especial (alunos com deficiência e necessidades específicas)
    'QT_MAT_BAS_FEM',	# Matrículas femininas na educação básica
    'QT_MAT_BAS_MASC',	# Matrículas masculinas na educação básica
    'QT_MAT_BAS_BRANCA',	# Matrículas de estudantes brancos
    'QT_MAT_BAS_PRETA',	# Matrículas de estudantes pretos
    'QT_MAT_BAS_PARDA',	# Matrículas de estudantes pardos
    'QT_MAT_BAS_AMARELA',	# Matrículas de estudantes amarelos (descendentes asiáticos)
    'QT_MAT_BAS_INDIGENA',	# Matrículas de estudantes indígenas

    # Alimentação e materiais (suporte básico)
    'IN_ALIMENTACAO',  # Oferece alimentação escolar (Sim/Não)
    'IN_MATERIAL_PED_CIENTIFICO',  # Possui material pedagógico científico (Sim/Não)
    'IN_MATERIAL_PED_ARTISTICAS',  # Possui material pedagógico artístico (Sim/Não)
    'IN_MATERIAL_PED_DESPORTIVA',  # Possui material pedagógico esportivo (Sim/Não)

    # Transporte escolar (crítico para zona rural)
    'QT_TRANSP_PUBLICO',  # Quantidade de transportes públicos escolares
    'QT_TRANSP_RESP_EST',  # Quantidade de transportes escolares responsabilidade do estado
    'QT_TRANSP_RESP_MUN',  # Quantidade de transportes escolares responsabilidade do município
]

def dados_tratados():
        
    # Agora leia apenas com as colunas disponíveis
    df = pd.read_csv("csv/dados.csv",
                    delimiter=";",
                    encoding="latin-1",
                    usecols=colunas_uteis,
                    low_memory=False)
    
    df.to_csv("dados/dados_inteiros.csv", sep=",", index=False, encoding="utf-8-sig")

    return df