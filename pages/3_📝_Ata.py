import streamlit as st
import pandas as pd
from services.repo_factory import get_repo
from services.notes_service import make_note, touch
from core.utils import parse_dt
from core.constants import RESULTADOS

st.set_page_config(page_title='Ata', page_icon='📝', layout='wide')
repo = get_repo()

st.title('📝 Ata da Visita')

clinics = repo.list_clinics()
visits = repo.list_visits()
if not visits:
    st.info('Nenhuma visita cadastrada.')
    st.stop()

clin_by_id = {c['id']: c for c in clinics}

pre = st.session_state.pop('selected_visit_id', None)
options=[]
for v in sorted(visits, key=lambda x: x.get('data_hora','')):
    c = clin_by_id.get(v.get('clinic_id'), {})
    dt = parse_dt(v.get('data_hora',''))
    label = f"{dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora','')} — {c.get('nome_cadastro','')}"
    options.append((label, v['id']))
labels=[o[0] for o in options]
map_id={o[0]: o[1] for o in options}
idx=0
if pre:
    for i,(_,vid) in enumerate(options):
        if vid==pre:
            idx=i
            break

sel = st.selectbox('Visita', labels, index=idx)
visit_id = map_id[sel]
visit = repo.get_visit(visit_id)
clinic = clin_by_id.get(visit.get('clinic_id'), {})

st.caption(f"Clínica: **{clinic.get('nome_cadastro','')}**")

note = repo.get_note_by_visit(visit_id)
creating=False
if not note:
    note = make_note(visit_id)
    creating=True

with st.form('note_form'):
    resultado = st.selectbox('Resultado', ['']+RESULTADOS, index=(['']+RESULTADOS).index(note.get('resultado') if note.get('resultado') in RESULTADOS else ''))
    pauta = st.text_input('Pauta', value=note.get('pauta',''))
    tratado = st.text_area('O que foi tratado', value=note.get('o_que_foi_tratado',''), height=140)
    acordos = st.text_area('Acordos', value=note.get('acordos',''), height=90)
    prox = st.text_area('Próximos passos', value=note.get('proximos_passos',''), height=110)
    save = st.form_submit_button('Salvar')

if save:
    note.update({'resultado': resultado, 'pauta': pauta, 'o_que_foi_tratado': tratado, 'acordos': acordos, 'proximos_passos': prox})
    touch(note, creating=creating)
    repo.upsert_note(note)
    st.success('Ata salva!')
