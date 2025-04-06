import requests
import streamlit as st

API_URL = "https://vb-sistemas.onrender.com"

def obter_processos():
    try:
        response = requests.get(f"{API_URL}/buscar-processos/?numero_processo=")
        return response.json().get("processos", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        st.error("Erro ao carregar processos.")
        return []

def calcular_estatisticas(processos):
    total_processos = len(processos)
    valor_medio = round(sum(p.get("valor_causa", 0) for p in processos) / total_processos, 2) if total_processos else 0
    tribunais_distintos = len(set(p.get("jurisdicao", "") for p in processos))
    
    return {"total_processos": total_processos, "valor_medio": valor_medio, "tribunais_distintos": tribunais_distintos}

def exibir_detalhes_processo(processo):
    with st.expander(f"📌 {processo.get('numero_processo', 'N/A')} | ⚖️ {', '.join(processo.get('advogados', ['N/A']))} | 🧑‍⚖️ {processo.get('exequente', 'N/A')} | 💼 {processo.get('executado', 'N/A')}"):
        for chave, valor in processo.items():
            st.write(f"**{chave.replace('_', ' ').capitalize()}:** {valor}")

def processar_pdf(uploaded_file):
    files = {"pdf": uploaded_file}
    response = requests.post(f"{API_URL}/processar-pdf/", files=files)
    if response.status_code == 200:
        resultado = response.json()
        st.success(resultado.get("mensagem", "Processo salvo!"))
        if "dados" in resultado:
            exibir_detalhes_processo(resultado["dados"])
    else:
        st.error("Erro ao processar o PDF.")

def verificar_status_api():
    """Verifica se a API está online e retorna o status."""
    try:
        response = requests.get(f"{API_URL}/docs", timeout=3)
        return "🟢 API Online" if response.status_code in [200, 307] else "🔴 API Offline"
    except requests.exceptions.RequestException:
        return "🔴 API Offline"

