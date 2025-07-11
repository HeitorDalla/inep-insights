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
    'IN_AGUA_REDE_PUBLICA',  # Água proveniente de rede pública (Sim/Não)
    'IN_AGUA_POCO_ARTESIANO',  # Utiliza poço artesiano (Sim/Não)
    'IN_AGUA_FONTE_RIO',  # Utiliza fonte/rio (Sim/Não)
    'IN_AGUA_INEXISTENTE',  # Não possui água (Sim/Não)
    'IN_ENERGIA_REDE_PUBLICA',  # Energia da rede pública (Sim/Não)
    'IN_ENERGIA_RENOVAVEL',  # Utiliza energia renovável (Sim/Não)
    'IN_ENERGIA_INEXISTENTE',  # Não possui energia elétrica (Sim/Não)
    'IN_ESGOTO_REDE_PUBLICA',  # Esgoto por rede pública (Sim/Não)
    'IN_ESGOTO_FOSSA',  # Possui algum tipo de fossa (Sim/Não)
    'IN_ESGOTO_INEXISTENTE',  # Não possui sistema de esgoto (Sim/Não)
    'IN_LIXO_SERVICO_COLETA',  # Lixo coletado por serviço de limpeza (Sim/Não)
    'IN_LIXO_QUEIMA',  # Queima o lixo (Sim/Não)
    'IN_LIXO_ENTERRA',  # Enterra o lixo (Sim/Não)
    'IN_LIXO_DESTINO_FINAL_PUBLICO',  # Lixo vai para destino público (Sim/Não)
    'IN_LIXO_DESCARTA_OUTRA_AREA',  # Descarta lixo em outra área (Sim/Não)

    # Espaços pedagógicos
    'IN_PATIO_COBERTO',  # Possui pátio coberto (Sim/Não)
    'IN_BIBLIOTECA',  # Possui biblioteca (Sim/Não)
    'IN_LABORATORIO_CIENCIAS',  # Possui laboratório de ciências (Sim/Não)
    'IN_LABORATORIO_INFORMATICA',  # Possui laboratório de informática (Sim/Não)
    'IN_QUADRA_ESPORTES',  # Possui quadra de esportes (Sim/Não)
    'IN_PARQUE_INFANTIL',  # Possui parque infantil (Sim/Não)
    'IN_SALA_PROFESSOR',  # Possui sala dos professores (Sim/Não)
    'IN_SALA_DIRETORIA',  # Possui sala de diretoria (Sim/Não)
    'IN_SALA_SECRETARIA',  # Possui sala de secretaria (Sim/Não)
    'IN_COZINHA',  # Possui cozinha (Sim/Não)
    'IN_REFEITORIO',  # Possui refeitório (Sim/Não)
    'IN_ALMOXARIFADO',  # Possui almoxarifado (Sim/Não)

    # Conectividade
    'IN_INTERNET',  # Possui acesso à internet (Sim/Não)
    'IN_BANDA_LARGA',  # Possui banda larga (Sim/Não)
    'IN_COMPUTADOR',  # Possui computadores (Sim/Não)
    'IN_EQUIP_MULTIMIDIA',  # Possui equipamentos multimídia (Sim/Não)
    'IN_EQUIP_TV',  # Possui televisores (Sim/Não)
    'QT_EQUIP_MULTIMIDIA',
    'QT_DESKTOP_ALUNO',
    'QT_COMP_PORTATIL_ALUNO',
    'QT_TABLET_ALUNO'

    # Recursos humanos (qualificação do ensino)
    'IN_PROF_BIBLIOTECARIO',  # Possui professor bibliotecário (Sim/Não)
    'IN_PROF_PEDAGOGIA',  # Possui professores de pedagogia (Sim/Não)
    'IN_PROF_SAUDE',  # Possui profissionais de saúde (Sim/Não)
    'IN_PROF_PSICOLOGO',  # Possui psicólogo (Sim/Não)
    'IN_PROF_ALIMENTACAO',  # Possui profissionais para alimentação (Sim/Não)
    'QT_PROF_ADMINSTRATIVOS',
    'QT_PROF_SERVICOS_GERAIS',
    'QT_PROF_SEGURANCA',
    'QT_PROF_GESTAO',
    'QT_PROF_ASSIST_SOCIAL',
    'IN_PROF_SEGURANCA',  # Possui profissionais de segurança (Sim/Não)
    'IN_PROF_ASSIST_SOCIAL',  # Possui assistente social (Sim/Não)
    'QT_MAT_BAS' # Total de matrículas na educação básica

    # Alimentação e materiais (suporte básico)
    'IN_ALIMENTACAO',  # Oferece alimentação escolar (Sim/Não)
    'IN_MATERIAL_PED_CIENTIFICO',  # Possui material pedagógico científico (Sim/Não)
    'IN_MATERIAL_PED_ARTISTICAS',  # Possui material pedagógico artístico (Sim/Não)
    'IN_MATERIAL_PED_DESPORTIVA',  # Possui material pedagógico esportivo (Sim/Não)
    'IN_MATERIAL_PED_JOGOS',  # Possui jogos pedagógicos (Sim/Não)

    # Transporte escolar (crítico para zona rural)
    'QT_TRANSP_PUBLICO',  # Quantidade de transportes públicos escolares
    'QT_TRANSP_RESP_EST',  # Quantidade de transportes escolares responsabilidade do estado
    'QT_TRANSP_RESP_MUN',  # Quantidade de transportes escolares responsabilidade do município

    # Educação indígena (comum em zonas rurais)
    'IN_EDUCACAO_INDIGENA',  # Oferece educação indígena (Sim/Não)
    'TP_INDIGENA_LINGUA',  # Tipo de língua indígena utilizada

    # Parcerias e convênios (fontes alternativas de recursos)
    'IN_PODER_PUBLICO_PARCERIA',  # Possui parceria com poder público (Sim/Não)
    'TP_PODER_PUBLICO_PARCERIA'  # Tipo de poder público parceiro
]

# Função para tratar os dados
def dados_tratados ():
    df = pd.read_csv("csv/dados.csv",
                    delimiter=";",          # Delimitador é ponto-e-vírgula
                    encoding="latin-1",     # Encoding correto para caracteres especiais
                    on_bad_lines="warn",    # Avisa sobre linhas problemáticas (opcional)
                    low_memory=False,        # Evita warnings de memória para arquivos grandes
                    usecols=colunas_uteis
    )

    return df # retornar os dados tratados