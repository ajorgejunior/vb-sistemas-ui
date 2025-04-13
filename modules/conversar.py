import streamlit as st
import requests
from utils import API_URL

def mostrar():
    st.title("🤖 Conversar com o Processo")

    numero = st.text_input("Número do processo:")

    if numero:
        st.subheader("Faça uma pergunta sobre esse processo:")
        pergunta = st.text_area("Pergunta")

        if st.button("Enviar pergunta"):
            with st.spinner("Enviando para a IA..."):
                try:
                    response = requests.post(
                        f"{API_URL}/conversar-processo",
                        json={"numero": numero, "pergunta": pergunta}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        resposta = data.get("resposta", "Sem resposta.")
                        resumo_limitado = data.get("resumo_limitado", False)

                        st.success("Resposta da IA:")
                        st.markdown(resposta)

                        if resumo_limitado:
                            st.warning("⚠️ O processo é muito grande. A IA analisou apenas partes essenciais (movimentações e anexos).")
                        else:
                            st.info("✅ A IA analisou o processo completo.")

                    else:
                        st.error(f"Erro ao consultar a IA: {response.status_code}")
                except Exception as e:
                    st.error(f"Erro de conexão com a API: {e}")

        st.subheader("🕓 Histórico de conversas com este processo")
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

