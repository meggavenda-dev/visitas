import streamlit as st

def get_backend() -> str:
    # default local
    return st.secrets.get("STORAGE_BACKEND", "local")

def get_supabase_url() -> str:
    return st.secrets.get("SUPABASE_URL", "")

def get_supabase_key() -> str:
    return st.secrets.get("SUPABASE_KEY", "")
