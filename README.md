# Programa de Visitas Médicas (Streamlit → Futuro App Mobile)

Este projeto é um MVP em Streamlit com arquitetura em camadas (UI → services → repositories) para facilitar a evolução para mobile.

## ✅ Funcionalidades
- **Hoje**: visitas do dia + próximos 7 dias + atrasadas.
- **Agendar**: criar, reagendar, cancelar e marcar como realizada.
- **Ata da Visita**: registrar o que foi tratado, acordos e próximos passos.
- **Clínicas**: cadastro, edição, importação de planilha (Excel) e contatos.

## 💾 Armazenamento
- **Padrão (sem configuração):** arquivos JSON em `data/`.
- **Opcional:** Supabase (Postgres) via `supabase-py`.

## 🚀 Como rodar
1. Crie um ambiente e instale dependências:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
pip install -r requirements.txt
```

2. (Opcional) Configure Supabase:
- Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`
- Preencha `SUPABASE_URL`, `SUPABASE_KEY` e `STORAGE_BACKEND="supabase"`
- Rode o SQL em `scripts/supabase_schema.sql`

3. Rode o app:

```bash
streamlit run app.py
```

## 📥 Importar clínicas via Excel
- Baixe o modelo em `assets/cadastro_clinicas_template.xlsx`.
- Preencha os campos extras (endereço, contatos etc.).
- Na aba **Clínicas**, use **Importar Excel**.

## 🧭 Próximos passos (evolução)
- Autenticação (Supabase Auth)
- Calendário/rota
- Notificações
- API (FastAPI) para o mobile
