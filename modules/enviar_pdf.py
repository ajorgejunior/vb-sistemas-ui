import streamlit as st
from utils import processar_pdf, processar_pdf_json

def mostrar():
    st.title("📄 Enviar PDF para Processamento")
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf", "Json"], help="Limite 10MB por arquivo")
    
    # Opção para escolher o tipo de extração
    tipo_extracao = st.radio("Selecione o tipo de extração", options=["GPT", "Json"])
    
    if uploaded_file and st.button("Enviar"):
        if tipo_extracao == "GPT":
            processar_pdf(uploaded_file)
        else:
            processar_pdf_json(uploaded_file)

