import streamlit as st
import pandas as pd
from datetime import datetime
from services.repo_factory import get_repo
from services.visits_service import make_visit, update_visit_ts
from core.utils import parse_dt
from core.constants import VisitStatus

st.set_page_config(page_title="Agendar", page_icon="📅", layout="wide")
repo = get_repo()

st.title("📅 Agendar / Gerenciar Visitas")

clinics = repo.list_clinics()
if not clinics:
    st.warning("Cadastre ou importe clínicas primeiro (aba Clínicas).")
    st.stop()

clinics_sorted = sorted(clinics, key=lambda x: x.get('nome_cadastro',''))
name_to_id = {c['nome_cadastro']: c['id'] for c in clinics_sorted}

edit_id = st.session_state.pop('edit_visit_id', None)
visit_edit = repo.get_visit(edit_id) if edit_id else None

with st.expander("➕ Criar / Editar visita", expanded=True):
    with st.form("visit_form", clear_on_submit=False):
        clinic_name = st.selectbox("Clínica", options=list(name_to_id.keys()),
                                 index=(list(name_to_id.keys()).index(next((c['nome_cadastro'] for c in clinics_sorted if c['id']==visit_edit.get('clinic_id')), list(name_to_id.keys())[0])) if visit_edit else 0))
        col1, col2 = st.columns(2)
        default_dt = parse_dt(visit_edit.get('data_hora','')) if visit_edit else None
        with col1:
            d = st.date_input("Data", value=(default_dt.date() if default_dt else datetime.now().date()))
        with col2:
            t = st.time_input("Hora", value=(default_dt.time().replace(second=0, microsecond=0) if default_dt else datetime.now().time().replace(second=0, microsecond=0)))
        objetivo = st.text_input("Objetivo", value=(visit_edit.get('objetivo','') if visit_edit else ''))
        assuntos = st.text_area("Assuntos/Tags (separe por vírgula)", value=(visit_edit.get('assuntos','') if visit_edit else ''), height=80)
        status = st.selectbox("Status", options=[s.value for s in VisitStatus], index=( [s.value for s in VisitStatus].index(visit_edit.get('status')) if visit_edit else 0 ))

        submitted = st.form_submit_button("Salvar")

    if submitted:
        clinic_id = name_to_id[clinic_name]
        dt = datetime.combine(d, t)
        if visit_edit:
            visit_edit['clinic_id'] = clinic_id
            visit_edit['data_hora'] = dt.isoformat(timespec='minutes')
            visit_edit['objetivo'] = objetivo
            visit_edit['assuntos'] = assuntos
            visit_edit['status'] = status
            update_visit_ts(visit_edit)
            repo.upsert_visit(visit_edit)
            st.success("Visita atualizada!")
        else:
            v = make_visit(clinic_id, dt, objetivo, assuntos)
            v['status'] = status
            repo.upsert_visit(v)
            st.success("Visita criada!")

st.divider()

st.subheader("📋 Todas as visitas")
visits = repo.list_visits()

# Enrich for display
clin_by_id = {c['id']: c for c in clinics}
rows = []
for v in visits:
    c = clin_by_id.get(v.get('clinic_id'), {})
    dt = parse_dt(v.get('data_hora',''))
    rows.append({
        'id': v.get('id'),
        'clínica': c.get('nome_cadastro',''),
        'data_hora': dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora',''),
        'status': v.get('status',''),
        'objetivo': v.get('objetivo',''),
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

colA, colB, colC = st.columns([2,2,3])
with colA:
    pick = st.selectbox("Selecionar visita (por ID)", options=[""] + list(df['id']) if not df.empty else [""])
with colB:
    if st.button("Editar") and pick:
        st.session_state['edit_visit_id'] = pick
        st.rerun()
with colC:
    if st.button("Excluir") and pick:
        repo.delete_visit(pick)
        st.success("Excluída.")
        st.rerun()
