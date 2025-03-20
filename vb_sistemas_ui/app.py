import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# Título do aplicativo
st.markdown("<h1 style='text-align: center;'>🔍 Consulta de Processos Jurídicos</h1>", unsafe_allow_html=True)
st.write("Selecione o tipo de dado e digite um termo para buscar informações.")

# Opções de filtro para pesquisa (ajustadas para corresponder à API)
tipos_pesquisa = {
    "Número do Processo": "numero_processo",
    "Tribunal": "tribunal",
    "Exequente": "exequente",
    "Executado": "executado",
    "Advogado": "advogado"
}

# Seletor para tipo de dado a ser pesquisado
tipo_dado = st.selectbox("Escolha o tipo de dado para pesquisa:", list(tipos_pesquisa.keys()))

# Campo de entrada para o termo de busca
termo_busca = st.text_input("Digite o termo para buscar...")

# Botão de busca
if st.button("Buscar", type="primary"):
    if termo_busca.strip() == "":
        st.warning("Por favor, digite um termo para buscar.")
    else:
        # Monta a URL para a requisição no backend
        backend_url = "https://vb-sistemas.onrender.com/buscar-processos"
        params = {tipos_pesquisa[tipo_dado]: termo_busca}

        # Faz a requisição ao backend
        response = requests.get(backend_url, params=params)

        # Processa a resposta
        if response.status_code == 200:
            data = response.json()

            # Verifica se há processos retornados
            if "processos" in data and isinstance(data["processos"], list):
                processos = data["processos"]

                if processos:
                    st.write(f"**{len(processos)} resultados encontrados:**")

                    # Exibir os processos de forma mais amigável
                    for processo in processos:
                        with st.container():
                            st.subheader(f"📌 Processo: {processo['numero_processo']}")
                            st.write(f"**📍 Tribunal:** {processo['tribunal']}")
                            st.write(f"**👤 Exequente:** {processo['exequente']}")
                            st.write(f"**⚖️ Executado:** {processo['executado']}")

                            # Verifica e converte JSON corretamente para lista
                            advogados = json.loads(processo["advogado"]) if isinstance(processo["advogado"], str) else processo["advogado"]
                            st.write(f"**👨‍⚖️ Advogados:** {', '.join(advogados) if advogados else 'Não informado'}")

                            st.write(f"**💰 Valor da Causa:** R$ {processo['valor_causa']:,.2f}")
                            st.write(f"**📌 Gratuidade:** {'Sim' if processo['gratuidade'] else 'Não'}")

                            # Exibir movimentações
                            movimentacoes = json.loads(processo["movimentacoes"]) if isinstance(processo["movimentacoes"], str) else processo["movimentacoes"]
                            st.write("📌 **Movimentações:**")
                            for mov in movimentacoes:
                                st.write(f"- {mov}")

                            st.markdown("---")  # Linha divisória entre processos

                else:
                    st.warning("Nenhum processo encontrado para esse critério.")
            else:
                st.error("Resposta inesperada do servidor.")
        else:
            st.error(f"Erro ao buscar processos: {response.status_code}")
