# Visitas Médicas (Streamlit)

MVP para controle de visitas médicas com:
- Hoje (visitas do dia + semana)
- Agendar/gerenciar visitas
- Ata da visita
- Cadastro de clínicas + importação via Excel

## Streamlit Cloud (importante)
Este repositório inclui `runtime.txt` fixando **Python 3.11** para evitar builds nativos (pandas/pydantic-core) no deploy.

## Rodar local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Supabase (opcional)
- Rode o SQL em `scripts/supabase_schema.sql`
- Crie `.streamlit/secrets.toml` com as chaves
