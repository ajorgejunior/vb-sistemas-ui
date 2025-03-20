import streamlit as st
import requests

# Definir URL da API backend
API_URL = "https://vb-sistemas.onrender.com"

# Configuração do layout
st.set_page_config(page_title="Consulta de Processos", layout="centered")
st.title("🔍 Consulta de Processos Jurídicos")
st.write("Selecione o tipo de dado e digite um termo para buscar informações.")

# Opções para tipo de pesquisa
opcoes_pesquisa = {
    "Número do Processo": "numero_processo",
    "Nome do Advogado": "advogado",
    "Tribunal": "tribunal",
    "Exequente": "exequente",
    "Executado": "executado"
}

# Seleção do tipo de pesquisa
tipo_pesquisa = st.selectbox("Escolha o tipo de dado para pesquisa:", list(opcoes_pesquisa.keys()))

# Campo de entrada para busca
search_query = st.text_input("Digite o termo para buscar...")

# Botão de busca
if st.button("Buscar"):
    if search_query:
        # Obter o parâmetro correto do dicionário
        parametro = opcoes_pesquisa[tipo_pesquisa]

        # Fazer requisição ao backend
        response = requests.get(f"{API_URL}/buscar-processos/", params={parametro: search_query})

        if response.status_code == 200:
            try:
                processos = response.json()
                if processos:
                    st.write(f"**{len(processos)} resultados encontrados:**")

                    # Criando um card para cada processo encontrado
                    for processo in processos:
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="border-radius: 10px; padding: 15px; background-color: #f8f9fa; 
                                            box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px;">
                                    <h4 style="color: #2c3e50;">📄 Processo: {processo.get("numero_processo", "N/A")}</h4>
                                    <p><strong>Tribunal:</strong> {processo.get("jurisdicao", "N/A")}</p>
                                    <p><strong>Órgão Julgador:</strong> {processo.get("orgao_julgador", "N/A")}</p>
                                    <p><strong>Classe:</strong> {processo.get("classe", "N/A")}</p>
                                    <p><strong>Assunto:</strong> {processo.get("assunto", "N/A")}</p>
                                    <p><strong>Exequente:</strong> {processo.get("exequente", "N/A")}</p>
                                    <p><strong>Executado:</strong> {processo.get("executado", "N/A")}</p>
                                    <p><strong>Advogados:</strong> {", ".join(processo.get("advogados", [])) if processo.get("advogados") else "N/A"}</p>
                                    <p><strong>Valor da Causa:</strong> R$ {processo.get("valor_causa", 0):,.2f}</p>
                                    <p><strong>Gratuidade:</strong> {"Sim" if processo.get("gratuidade") else "Não"}</p>
                                    <p><strong>Últimas Movimentações:</strong></p>
                                    <ul>
                                        {''.join(f'<li>{mov["data"]}: {mov["descricao"]}</li>' for mov in processo.get("movimentacoes", []))}
                                    </ul>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                else:
                    st.warning("Nenhum processo encontrado.")
            except Exception as e:
                st.error(f"Erro ao processar resposta do servidor: {e}")
        else:
            st.error(f"Erro na requisição: {response.status_code}")
    else:
        st.warning("Digite um termo para buscar.")
