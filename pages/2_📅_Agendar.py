import streamlit as st
import pandas as pd
from datetime import datetime
from services.repo_factory import get_repo
from services.visits_service import make_visit, touch
from core.utils import parse_dt
from core.constants import VisitStatus

st.set_page_config(page_title="Agendar", page_icon="📅", layout="wide")
repo = get_repo()

st.title("📅 Agendar")

clinics = repo.list_clinics()
if not clinics:
    st.warning('Cadastre ou importe clínicas primeiro (aba Clínicas).')
    st.stop()

clinics_sorted = sorted(clinics, key=lambda x: x.get('nome_cadastro',''))
name_to_id = {c['nome_cadastro']: c['id'] for c in clinics_sorted}

edit_id = st.session_state.pop('edit_visit_id', None)
visit_edit = repo.get_visit(edit_id) if edit_id else None

with st.form('visit_form'):
    clinic_name = st.selectbox('Clínica', list(name_to_id.keys()),
                              index=0 if not visit_edit else list(name_to_id.values()).index(visit_edit.get('clinic_id')))
    col1,col2 = st.columns(2)
    default_dt = parse_dt(visit_edit.get('data_hora','')) if visit_edit else None
    d = col1.date_input('Data', value=(default_dt.date() if default_dt else datetime.now().date()))
    t = col2.time_input('Hora', value=(default_dt.time().replace(second=0, microsecond=0) if default_dt else datetime.now().time().replace(second=0, microsecond=0)))
    objetivo = st.text_input('Objetivo', value=(visit_edit.get('objetivo','') if visit_edit else ''))
    assuntos = st.text_area('Assuntos', value=(visit_edit.get('assuntos','') if visit_edit else ''), height=80)
    status = st.selectbox('Status', [s.value for s in VisitStatus], index=0 if not visit_edit else [s.value for s in VisitStatus].index(visit_edit.get('status')))
    save = st.form_submit_button('Salvar')

if save:
    clinic_id = name_to_id[clinic_name]
    dt = datetime.combine(d, t)
    if visit_edit:
        visit_edit.update({'clinic_id': clinic_id, 'data_hora': dt.isoformat(timespec='minutes'), 'objetivo': objetivo, 'assuntos': assuntos, 'status': status})
        touch(visit_edit)
        repo.upsert_visit(visit_edit)
        st.success('Visita atualizada!')
    else:
        v = make_visit(clinic_id, dt, objetivo, assuntos, status)
        repo.upsert_visit(v)
        st.success('Visita criada!')

st.divider()

visits = repo.list_visits()
clin_by_id = {c['id']: c for c in clinics}
rows=[]
for v in visits:
    c = clin_by_id.get(v.get('clinic_id'), {})
    dt = parse_dt(v.get('data_hora',''))
    rows.append({'id': v.get('id'), 'clínica': c.get('nome_cadastro',''), 'data_hora': dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora',''), 'status': v.get('status','')})

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

pick = st.selectbox('Selecionar visita (ID)', [''] + list(df['id']) if not df.empty else [''])
colA,colB = st.columns(2)
if colA.button('Editar') and pick:
    st.session_state['edit_visit_id'] = pick
    st.rerun()
if colB.button('Excluir') and pick:
    repo.delete_visit(pick)
    st.success('Excluída.')
    st.rerun()
