import streamlit as st
import pandas as pd
from utils import obter_processos, calcular_estatisticas

def mostrar():
    st.title("📊 Painel de Estatísticas (em construção)")
    processos = obter_processos()
    estatisticas = calcular_estatisticas(processos)

    col1, col2, col3 = st.columns(3)
    col1.metric("📂 Total de Processos", estatisticas["total_processos"])
    col2.metric("💰 Valor Médio das Causas (R$)", estatisticas["valor_medio"])
    col3.metric("🏛️ Tribunais Distintos", estatisticas["tribunais_distintos"])

    # Criar lista de advogados e tribunais
    advogados_disponiveis = sorted({adv for p in processos for adv in p.get("advogados", [])})
    tribunais_disponiveis = sorted({p.get("jurisdicao", "Desconhecido") for p in processos})
    
    advogados_disponiveis.insert(0, "Todos")
    tribunais_disponiveis.insert(0, "Todos")

    # Filtros
    st.subheader("🔎 Filtrar Processos")
    col1, col2 = st.columns(2)
    
    advogado_selecionado = col1.selectbox("Escolha um advogado:", advogados_disponiveis)
    tribunal_selecionado = col2.selectbox("Escolha um tribunal:", tribunais_disponiveis)

    # Aplicar filtros
    processos_filtrados = [p for p in processos if (advogado_selecionado == "Todos" or advogado_selecionado in p.get("advogados", [])) and
                           (tribunal_selecionado == "Todos" or p.get("jurisdicao") == tribunal_selecionado)]

    # Exibir tabela filtrada
    df = pd.DataFrame(processos_filtrados).drop(columns=["id", "data_criacao"], errors="ignore")
    # Defina a ordem desejada das colunas
    ordem_colunas = ["numero_processo", "instancia", "assunto", "exequente", "executado", "valor_causa", "jurisdicao", "orgao_julgador", "classe", "advogados", "resumo_processo", "competencia", "movimentacoes"]

    # Reordene o DataFrame conforme a lista
    df = df[ordem_colunas]

    st.dataframe(df) if not df.empty else st.warning("Nenhum processo encontrado.")

