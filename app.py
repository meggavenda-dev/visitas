import streamlit as st

st.set_page_config(page_title="Visitas Médicas", page_icon="🩺", layout="wide")
st.title("🩺 Visitas Médicas")
st.caption("MVP em Streamlit (local JSON ou Supabase).")

st.markdown("""
Use o menu lateral:
- **Hoje**: visão do dia e da semana
- **Agendar**: cria/edita visitas
- **Ata**: registro da reunião
- **Clínicas**: cadastro e importação
""")
