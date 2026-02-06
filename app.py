import streamlit as st

st.set_page_config(
    page_title="Visitas Médicas",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Programa de Visitas Médicas")
st.caption("MVP em Streamlit com armazenamento local (JSON) ou Supabase.")

st.markdown("""
### Como usar
- Use o menu lateral para navegar entre as abas.
- Comece cadastrando/ importando **Clínicas**.
- Depois agende visitas e registre as **Atas**.
""")

st.info("Dica: se você quiser usar Supabase, configure `.streamlit/secrets.toml` e rode o SQL em `scripts/supabase_schema.sql`.")
