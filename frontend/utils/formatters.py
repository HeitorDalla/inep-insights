# # Função auxiliar para formatação de grandes números

def format_number(value: int) -> str:
    """
    Formata números com separadores brasileiros e sufixos apropriados.
    - Valores >= 1.000.000: mostra em milhões com 1 casa decimal
    - Valores >= 1.000: mostra em milhares com 1 casa decimal  
    - Valores < 1.000: mostra o número completo
    """
    
    if value >= 1000000:  # 1 milhão ou mais
        base = value / 1000000
        if base >= 10:  # 10M ou mais - sem casa decimal
            s = f"{base:,.0f}"
        else:  # Menos de 10M - com 1 casa decimal
            s = f"{base:,.1f}"
        # Troca separadores para formato brasileiro
        s = s.replace(",", "@").replace(".", ",").replace("@", ".")
        return f"{s} mi"
    
    elif value >= 1000:  # 1 mil ou mais
        base = value / 1000
        if base >= 10:  # 10k ou mais - sem casa decimal
            s = f"{base:,.0f}"
        else:  # Menos de 10k - com 1 casa decimal
            s = f"{base:,.1f}"
        # Troca separadores para formato brasileiro
        s = s.replace(",", "@").replace(".", ",").replace("@", ".")
        return f"{s} mil"
    
    else:  # Menos de 1000
        s = f"{value:,.0f}"
        return s.replace(",", "@").replace(".", ",").replace("@", ".")
    
# Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
def bool_to_text(flag: int) -> str:
    return "Sim ✅" if bool(flag) else "Não ❌"