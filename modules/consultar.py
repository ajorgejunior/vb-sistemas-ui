import streamlit as st
import requests
from utils import API_URL, exibir_detalhes_processo
from modules.editar_processo import mostrar_formulario_edicao

def mostrar():
    st.title("🔍 Consulta de Processos Jurídicos")

    # Lê parâmetro da URL, ex: ?numero=0000000-00.0000.0.00.0000
    query_params = st.query_params
    numero_param = query_params.get("numero", None)

    # Estado inicial
    if "resultados_busca" not in st.session_state:
        st.session_state.resultados_busca = []
    if "processo_editando" not in st.session_state:
        st.session_state.processo_editando = None
    if "confirmar_delete_id" not in st.session_state:
        st.session_state.confirmar_delete_id = None

    termo_busca = st.text_input(
        "Digite um número de processo, advogado, tribunal...",
        value=numero_param or ""
    )
    tipo_busca = st.selectbox(
        "Escolha o tipo de dado para pesquisa:",
        ["numero_processo", "advogado", "executado", "exequente", "tribunal"]
    )

    # Executa busca automaticamente se veio da URL
    if numero_param and not st.session_state.resultados_busca:
        response = requests.get(f"{API_URL}/buscar-processos/?numero_processo={numero_param}")
        if response.status_code == 200:
            processos = response.json().get("processos", [])
            st.session_state.resultados_busca = processos

    # Botão manual
    if st.button("Buscar") and termo_busca:
        response = requests.get(f"{API_URL}/buscar-processos/?{tipo_busca}={termo_busca}")
        if response.status_code == 200:
            processos = response.json().get("processos", [])
            st.session_state.resultados_busca = processos
            st.session_state.processo_editando = None
            st.session_state.confirmar_delete_id = None
        else:
            st.error("Erro ao buscar processos.")

    for i, processo in enumerate(st.session_state.resultados_busca):
        with st.container():
            col_titulo, col_botoes = st.columns([8, 2])
            with col_titulo:
                st.markdown(
                    f"**📌 {processo['numero_processo']}** &nbsp;&nbsp; "
                    f"⚖️ {', '.join(processo.get('advogados', []))} &nbsp;&nbsp; "
                    f"🧑‍⚖️ {processo.get('exequente', '')} &nbsp;&nbsp; "
                    f"💼 {processo.get('executado', '')}",
                    unsafe_allow_html=True
                )

            with col_botoes:
                col1, col2 = st.columns(2)
                if col1.button("✏️", key=f"editar_{i}"):
                    st.session_state.processo_editando = processo["id"]
                if col2.button("🗑️", key=f"deletar_{i}"):
                    st.session_state.confirmar_delete_id = processo["id"]

            if st.session_state.get("confirmar_delete_id") == processo["id"]:
                st.warning("Tem certeza que deseja excluir este processo?")
                col_c1, col_c2 = st.columns(2)
                if col_c1.button("✅ Confirmar", key=f"confirma_excluir_{i}"):
                    del_response = requests.delete(f"{API_URL}/processos/{processo['id']}")
                    if del_response.status_code == 200:
                        st.success("Processo deletado com sucesso!")
                        st.session_state.resultados_busca = [
                            p for p in st.session_state.resultados_busca if p["id"] != processo["id"]
                        ]
                        st.session_state.confirmar_delete_id = None
                        st.rerun()
                    else:
                        st.error("Erro ao deletar processo.")
                if col_c2.button("❌ Cancelar", key=f"cancela_excluir_{i}"):
                    st.session_state.confirmar_delete_id = None

            with st.expander("🔎 Ver detalhes"):
                exibir_detalhes_processo(processo)

            if st.session_state.processo_editando == processo["id"]:
                st.markdown("---")
                mostrar_formulario_edicao(processo)
                st.markdown("---")

