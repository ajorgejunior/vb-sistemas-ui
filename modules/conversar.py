import streamlit as st
import requests
from utils import API_URL

def mostrar():
    st.title("🤖 Conversar com o Processo")

    numero = st.text_input("Número do processo:")

    if numero:
        st.subheader("🧠 Escolha uma análise inteligente:")
        col1, col2, col3 = st.columns(3)

        analise_tipo = None

        with col1:
            if st.button("📜 Resumo e histórico"):
                analise_tipo = "resumo"
            if st.button("📎 Resumo dos anexos"):
                analise_tipo = "anexos"

        with col2:
            if st.button("⏳ Prazos e pendências"):
                analise_tipo = "prazos"
            if st.button("📊 Relatório para cliente"):
                analise_tipo = "relatorio"

        with col3:
            if st.button("🧠 Insights estratégicos"):
                analise_tipo = "insights"

        if analise_tipo:
            with st.spinner("Analisando com IA..."):
                try:
                    response = requests.post(
                        f"{API_URL}/conversar-processo",
                        json={"numero": numero, "tipo": analise_tipo}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Resposta da IA:")
                        st.markdown(data.get("resposta", "Sem resposta."))

                        if data.get("resumo_limitado"):
                            st.warning("⚠️ O processo é muito grande. A IA analisou apenas partes essenciais (movimentações e anexos).")
                        else:
                            st.info("✅ A IA analisou o processo completo.")
                    else:
                        st.error("Erro ao processar a análise.")
                except Exception as e:
                    st.error(f"Erro de conexão com a API: {e}")

        st.subheader("💬 Histórico de conversas com este processo")
        try:
            historico = requests.get(f"{API_URL}/conversas-ia/{numero}")
            if historico.status_code == 200:
                conversas = historico.json()
                if not conversas:
                    st.info("Ainda não há conversas registradas.")
                for conv in conversas:
                    with st.expander(f"{conv['data']}"):
                        st.markdown(f"**Pergunta:** {conv['pergunta']}")
                        st.markdown(f"**Resposta:** {conv['resposta']}")
            else:
                st.warning("Não foi possível carregar o histórico de conversas.")
        except Exception as e:
            st.error(f"Erro ao buscar histórico: {e}")

