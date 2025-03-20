import streamlit as st
import requests
import json

def buscar_processos(tipo_busca, termo):
    url = f"https://vb-sistemas.onrender.com/buscar-processos/?{tipo_busca}={termo}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def enviar_pdf(arquivo):
    url = "https://vb-sistemas.onrender.com/processar-pdf/"
    files = {"pdf": arquivo}
    response = requests.post(url, files=files)
    return response

st.set_page_config(page_title="VB Sistemas - Consulta Jurídica", page_icon="🔍", layout="wide")

menu = st.sidebar.radio("Navegação", ["Consultar Processos", "Enviar PDF para Processamento"])

if menu == "Consultar Processos":
    st.markdown("# 🔍 Consulta de Processos Jurídicos")
    st.write("Selecione o tipo de dado e digite um termo para buscar informações.")
    
    opcoes_busca = {
        "Número do Processo": "numero_processo",
        "Advogado": "advogado",
        "Executado": "executado",
        "Exequente": "exequente",
        "Tribunal/Órgão Julgador": "tribunal"
    }
    
    tipo_busca = st.selectbox("Escolha o tipo de dado para pesquisa:", list(opcoes_busca.keys()))
    termo_busca = st.text_input("Digite o termo para buscar...")
    
    if st.button("Buscar"):
        if termo_busca:
            resultados = buscar_processos(opcoes_busca[tipo_busca], termo_busca)
            if resultados and "processos" in resultados and resultados["processos"]:
                st.write(f"**{len(resultados['processos'])} resultados encontrados:**")
                for processo in resultados["processos"]:
                    with st.expander(f"📌 {processo['numero_processo']} - {processo['orgao_julgador']}"):
                        st.markdown(f"""
                        **🏛️ Tribunal:** {processo["jurisdicao"]}  
                        **📂 Classe:** {processo["classe"]}  
                        **📝 Assunto:** {processo["assunto"]}  
                        **💰 Valor da Causa:** R$ {processo["valor_causa"]:.2f}  
                        **⚖️ Exequente:** {processo["exequente"]}  
                        **⚖️ Executado:** {processo["executado"]}  
                        **📅 Data de Criação:** {processo["data_criacao"]}  
                        """)
                        
                        if "movimentacoes" in processo and isinstance(processo["movimentacoes"], list):
                            st.write("### 📜 Movimentações:")
                            for mov in processo["movimentacoes"]:
                                st.markdown(f"- {mov}")
            else:
                st.warning("Nenhum processo encontrado para o termo informado.")
        else:
            st.error("Por favor, digite um termo para buscar.")

elif menu == "Enviar PDF para Processamento":
    st.markdown("# 📤 Enviar PDF para Processamento")
    st.write("Envie um arquivo PDF contendo informações sobre processos jurídicos para extração e cadastro no sistema.")
    
    arquivo_pdf = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    
    if arquivo_pdf is not None:
        if st.button("Enviar"):
            response = enviar_pdf(arquivo_pdf)
            if response.status_code == 200:
                resposta_json = response.json()
                if "mensagem" in resposta_json and "dados" in resposta_json:
                    if resposta_json["mensagem"] == "Processo já existe no banco":
                        st.warning("O processo já existe no banco de dados e não foi cadastrado novamente.")
                        
                        processo = resposta_json["dados"]
                        with st.expander("Detalhes do Processo Existente"):
                            st.markdown(f"""
                                **📌 Número do Processo:** {processo["numero_processo"]}  
                                **🏛️ Tribunal:** {processo["jurisdicao"]}  
                                **⚖️ Órgão Julgador:** {processo["orgao_julgador"]}  
                                **📂 Classe:** {processo["classe"]}  
                                **📝 Assunto:** {processo["assunto"]}  
                                **💰 Valor da Causa:** R$ {processo["valor_causa"]:.2f}  
                                **⚖️ Exequente:** {processo["exequente"]}  
                                **⚖️ Executado:** {processo["executado"]}  
                                **📅 Data de Criação:** {processo["data_criacao"]}  
                            """)
                            
                            if "movimentacoes" in processo and isinstance(processo["movimentacoes"], list):
                                st.write("### 📜 Movimentações:")
                                for mov in processo["movimentacoes"]:
                                    st.markdown(f"- {mov}")
                    else:
                        st.success("Arquivo processado e salvo no banco de dados com sucesso!")
                else:
                    st.success("Arquivo processado e salvo no banco de dados com sucesso!")
            else:
                st.error(f"Erro ao enviar o arquivo. Código {response.status_code} - {response.text}")
