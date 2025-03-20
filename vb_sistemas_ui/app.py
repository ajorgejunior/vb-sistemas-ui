import streamlit as st
import requests

# Configuração da interface
st.set_page_config(page_title="Consulta de Processos Jurídicos", page_icon="🔍", layout="wide")

# URL do backend
API_URL = "https://vb-sistemas.onrender.com"

def verificar_status_api():
    """Verifica se a API está online e retorna o status."""
    try:
        response = requests.get(f"{API_URL}/docs", timeout=3)  # Testando a rota de documentação
        if response.status_code in [200, 307]:  # 307 ocorre se houver redirecionamento
            return "🟢 API Online"
        else:
            return "🔴 API Offline"
    except requests.exceptions.RequestException:
        return "🔴 API Offline"

def exibir_detalhes_processo(processo):
    """Exibe os detalhes do processo dentro de um container expansível."""
    with st.expander(f"📌 Processo: {processo.get('numero_processo', 'N/A')} | ⚖️ Advogado(s): {', '.join(processo.get('advogados', ['N/A']))}"):
        st.write(f"**⚖️ Instância:** {processo.get('instancia', 'N/A')}")
        st.write(f"**🏩 Tribunal:** {processo.get('jurisdicao', 'N/A')}")
        st.write(f"**📍 Órgão Julgador:** {processo.get('orgao_julgador', 'N/A')}")
        st.write(f"**📝 Competência:** {processo.get('competencia', 'N/A')}")
        st.write(f"**📂 Classe:** {processo.get('classe', 'N/A')}")
        st.write(f"**📁 Assunto:** {processo.get('assunto', 'N/A')}")
        st.write(f"**👨‍⚖️ Exequente:** {processo.get('exequente', 'N/A')}")
        st.write(f"**👤 Executado:** {processo.get('executado', 'N/A')}")
        st.write(f"**💰 Valor da Causa:** R$ {processo.get('valor_causa', 'N/A')}")
        st.write(f"**📛 Gratuidade:** {'Sim' if processo.get('gratuidade', False) else 'Não'}")

        if "movimentacoes" in processo:
            movimentacoes = processo["movimentacoes"]
            if isinstance(movimentacoes, list):
                movimentacoes = "\n".join(movimentacoes)
            st.write(f"**📌 Movimentações:** \n{movimentacoes}")

        if "data_criacao" in processo:
            st.write(f"**📅 Data de Criação:** {processo['data_criacao']}")

def processar_pdf(uploaded_file):
    """Envia um arquivo PDF para processamento no backend."""
    files = {"pdf": uploaded_file}
    response = requests.post(f"{API_URL}/processar-pdf/", files=files)
    if response.status_code == 200:
        resultado = response.json()
        if "mensagem" in resultado and "dados" in resultado:
            st.success(resultado["mensagem"])
            exibir_detalhes_processo(resultado["dados"])
        elif "mensagem" in resultado:
            st.warning(resultado["mensagem"])
        else:
            st.success("Arquivo processado e salvo no banco de dados com sucesso!")
    else:
        st.error("Erro ao processar o PDF. Tente novamente.")

def main():
    st.sidebar.title("Menu")
    pagina = st.sidebar.radio("Escolha uma opção", ["Consultar Processos", "Enviar PDF para Processamento"])
    
    if pagina == "Consultar Processos":
        st.title("🔍 Consulta de Processos Jurídicos")
        termo_busca = st.text_input("Digite um número de processo, advogado, tribunal...")
        tipo_busca = st.selectbox("Escolha o tipo de dado para pesquisa:", ["numero_processo", "advogado", "executado", "exequente", "tribunal"])
        
        if st.button("Buscar"):
            if termo_busca:
                response = requests.get(f"{API_URL}/buscar-processos/?{tipo_busca}={termo_busca}")
                if response.status_code == 200:
                    resultado = response.json()
                    processos = resultado.get("processos", [])
                    if processos:
                        for processo in processos:
                            exibir_detalhes_processo(processo)
                    else:
                        st.warning("Nenhum processo encontrado.")
                else:
                    st.error("Erro ao buscar processos.")
            else:
                st.warning("Digite um termo para busca.")
    
    elif pagina == "Enviar PDF para Processamento":
        st.title("📄 Enviar PDF para Processamento")
        uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"], help="Limite 200MB por arquivo")
        
        if uploaded_file and st.button("Enviar"):
            processar_pdf(uploaded_file)

    # Rodapé com status da API
    st.markdown("---")
    api_status = verificar_status_api()
    st.markdown(f"<p style='text-align: center; color: gray;'>📡 Status da API: {api_status}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
