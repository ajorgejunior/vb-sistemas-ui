import requests
import streamlit as st
import math

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

#def exibir_detalhes_processo(processo):
#    campos_ocultos = {"id", "data_criacao", "data_atualizacao"}
#    for chave, valor in processo.items():
#        if chave in campos_ocultos:
#            continue
#        if isinstance(valor, list):
#            valor = ", ".join(map(str, valor))
#        st.write(f"**{chave.replace('_', ' ').capitalize()}:** {valor}")

def exibir_detalhes_processo(processo):
    campos_ocultos = {"id", "data_criacao", "data_atualizacao"}
    
    # Exibe primeiro todos os campos, exceto "movimentacoes"
    for chave, valor in processo.items():
        if chave in campos_ocultos or chave == "movimentacoes":
            continue
        if isinstance(valor, list):
            valor = ", ".join(map(str, valor))
        st.write(f"**{chave.replace('_', ' ').capitalize()}:** {valor}")
    
    # Agora exibe as movimentações (se existirem) ao final
    if "movimentacoes" in processo:
        valor = processo["movimentacoes"]
        if isinstance(valor, list):
            movimentos = valor
        elif isinstance(valor, str):
            movimentos = valor.split(",")
        else:
            movimentos = [valor]
        movimentos = [mov.strip() for mov in movimentos if mov.strip()]

        itens_por_pagina = 5
        total_paginas = math.ceil(len(movimentos) / itens_por_pagina)

        mov_page_key = f"mov_page_{processo.get('id', 'sem_id')}"
        if mov_page_key not in st.session_state:
            st.session_state[mov_page_key] = 1
        if st.session_state[mov_page_key] < 1:
            st.session_state[mov_page_key] = 1
        elif st.session_state[mov_page_key] > total_paginas:
            st.session_state[mov_page_key] = total_paginas

        inicio = (st.session_state[mov_page_key] - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina

        st.markdown("**Movimentações:**")
        for mov in movimentos[inicio:fim]:
            st.write(f"- {mov}")

        # Só exibe paginação se houver mais de 5 movimentações
        if total_paginas > 1:
            col_prev, col_pages, col_next = st.columns([1, 6, 1])

            with col_prev:
                if st.button("◀️", key=f"prev_{processo['id']}"):
                    if st.session_state[mov_page_key] > 1:
                        st.session_state[mov_page_key] -= 1
                        st.rerun()

            with col_next:
                if st.button("▶️", key=f"next_{processo['id']}"):
                    if st.session_state[mov_page_key] < total_paginas:
                        st.session_state[mov_page_key] += 1
                        st.rerun()

            with col_pages:
                page_cols = st.columns(total_paginas)
                for page in range(1, total_paginas + 1):
                    with page_cols[page - 1]:
                        if page == st.session_state[mov_page_key]:
                            st.markdown(f"<b>{page}</b>", unsafe_allow_html=True)
                        else:
                            if st.button(f"{page}", key=f"page_{processo['id']}_{page}"):
                                st.session_state[mov_page_key] = page
                                st.rerun()


def exibir_detalhes_processo_cadastro(processo: dict):
    st.subheader("✅ Processo cadastrado com sucesso!")

    numero = processo.get("numero_processo", "Não informado")
    instancia = processo.get("instancia", "Não informada")
    jurisdicao = processo.get("jurisdicao", "Não informada")
    orgao_julgador = processo.get("orgao_julgador", "Não informado")
    competencia = processo.get("competencia", "Não informada")
    classe = processo.get("classe", "Não informada")
    assunto = processo.get("assunto", "Não informado")
    valor = processo.get("valor_causa", 0.0)
    gratuidade = "Sim" if processo.get("gratuidade", False) else "Não"

    st.markdown(f"**Número do Processo:** {numero}")
    st.markdown(f"**Instância:** {instancia}")
    st.markdown(f"**Jurisdicao:** {jurisdicao}")
    st.markdown(f"**Órgão Julgador:** {orgao_julgador}")
    st.markdown(f"**Competência:** {competencia}")
    st.markdown(f"**Classe:** {classe}")
    st.markdown(f"**Assunto:** {assunto}")
    st.markdown(f"**Valor da Causa:** R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.markdown(f"**Gratuidade:** {gratuidade}")

    exequente = processo.get("exequente", "Não informado")
    executado = processo.get("executado", "Não informado")
    advogados = processo.get("advogados", [])

    st.markdown("**Exequente:** " + exequente)
    st.markdown("**Executado:** " + executado)
    if advogados:
        st.markdown("**Advogados:**")
        for adv in advogados:
            st.markdown(f"- {adv}")

    st.markdown("---")
    st.markdown("**Resumo do Processo:**")
    st.info(processo.get("resumo_processo", "Sem resumo."))

    st.markdown("**Movimentações Recentes:**")
    for mov in processo.get("movimentacoes", [])[:10]:
        st.markdown(f"- {mov}")

def processar_pdf(uploaded_file):
    files = {"pdf": uploaded_file}
    response = requests.post(f"{API_URL}/processar-pdf/", files=files)
    if response.status_code == 200:
        resultado = response.json()
        st.success(resultado.get("mensagem", "Processo salvo!"))
        if "dados" in resultado:
            exibir_detalhes_processo_cadastro(resultado["dados"])
    else:
        st.error("Erro ao processar o PDF.")

def processar_pdf_json(uploaded_file):
    files = {"json_file": uploaded_file}
    response = requests.post(f"{API_URL}/upload-json/", files=files)
    if response.status_code == 200:
        resultado = response.json()
        st.success(resultado.get("mensagem", "Processo salvo!"))
        if "dados" in resultado:
            exibir_detalhes_processo_cadastro(resultado["dados"])
    else:
        st.error("Erro ao processar o Json.")

def verificar_status_api():
    try:
        response = requests.get(f"{API_URL}/docs", timeout=3)
        return "🟢 API Online" if response.status_code in [200, 307] else "🔴 API Offline"
    except requests.exceptions.RequestException:
        return "🔴 API Offline"

