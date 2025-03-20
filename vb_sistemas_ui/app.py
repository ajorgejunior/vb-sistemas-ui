import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Sistema Jurídico", page_icon="⚖️", layout="wide")

# Sidebar para navegação entre módulos
st.sidebar.title("📌 Menu")
modulo = st.sidebar.radio("Escolha uma opção:", ["🔍 Consulta de Processos", "📄 Cadastrar Processo (PDF)"])

# URL do backend
BACKEND_URL = "https://vb-sistemas.onrender.com"

# 🟢 **Consulta de Processos**
if modulo == "🔍 Consulta de Processos":
    st.markdown("<h1 style='text-align: center;'>🔍 Consulta de Processos Jurídicos</h1>", unsafe_allow_html=True)
    st.write("Selecione o tipo de dado e digite um termo para buscar informações.")

    # Opções de filtro para pesquisa (conforme API)
    tipos_pesquisa = {
        "Número do Processo": "numero_processo",
        "Tribunal": "jurisdicao",
        "Exequente": "exequente",
        "Executado": "executado",
        "Advogado": "advogado"
    }

    # Seletor para o tipo de pesquisa
    tipo_dado = st.selectbox("Escolha o tipo de dado para pesquisa:", list(tipos_pesquisa.keys()))

    # Campo de entrada para pesquisa
    termo_busca = st.text_input("Digite o termo para buscar...")

    # Botão de busca
    if st.button("Buscar", type="primary"):
        if termo_busca.strip() == "":
            st.warning("Por favor, digite um termo para buscar.")
        else:
            params = {tipos_pesquisa[tipo_dado]: termo_busca}
            response = requests.get(f"{BACKEND_URL}/buscar-processos", params=params)

            if response.status_code == 200:
                data = response.json()
                processos = data.get("processos", [])

                if processos:
                    st.write(f"**{len(processos)} resultados encontrados:**")

                    # Exibir cada processo em um card
                    for processo in processos:
                        with st.container():
                            st.subheader(f"📌 Processo: {processo.get('numero_processo', 'Não informado')}")
                            st.write(f"**📍 Tribunal:** {processo.get('jurisdicao', 'Não informado')}")
                            st.write(f"**👤 Exequente:** {processo.get('exequente', 'Não informado')}")
                            st.write(f"**⚖️ Executado:** {processo.get('executado', 'Não informado')}")

                            # Converter JSON de advogados corretamente
                            advogados = json.loads(processo["advogados"]) if isinstance(processo["advogados"], str) else processo["advogados"]
                            st.write(f"**👨‍⚖️ Advogados:** {', '.join(advogados) if advogados else 'Não informado'}")

                            st.write(f"**💰 Valor da Causa:** R$ {processo.get('valor_causa', 0):,.2f}")
                            st.write(f"**📌 Gratuidade:** {'Sim' if processo.get('gratuidade', False) else 'Não'}")

                            # Exibir movimentações
                            movimentacoes = json.loads(processo["movimentacoes"]) if isinstance(processo["movimentacoes"], str) else processo["movimentacoes"]
                            st.write("📌 **Movimentações:**")
                            for mov in movimentacoes:
                                st.write(f"- {mov}")

                            st.markdown("---")  # Linha divisória entre processos

                else:
                    st.warning("Nenhum processo encontrado para esse critério.")
            else:
                st.error(f"Erro ao buscar processos: {response.status_code}")

# 🟡 **Cadastro de Processo via PDF**
elif modulo == "📄 Cadastrar Processo (PDF)":
    st.markdown("<h1 style='text-align: center;'>📄 Cadastro de Processo via PDF</h1>", unsafe_allow_html=True)
    st.write("Faça o upload de um arquivo PDF para extrair os dados e cadastrar o processo no banco de dados.")

    # Campo de upload de PDF
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

    if uploaded_file is not None:
        st.write(f"📂 Arquivo selecionado: **{uploaded_file.name}**")
        
        if st.button("📤 Enviar para Processamento"):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/processar-pdf", files=files)

            if response.status_code == 200:
                resultado = response.json()
                if "mensagem" in resultado:
                    st.success(f"✅ {resultado['mensagem']}")
                else:
                    st.success("✅ Arquivo processado com sucesso!")
            else:
                st.error("❌ Erro ao processar o PDF. Verifique o arquivo e tente novamente.")

# 🟠 **Rodapé**
st.sidebar.markdown("---")
st.sidebar.write("🔹 Desenvolvido por VB Sistemas")
