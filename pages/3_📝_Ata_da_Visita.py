import streamlit as st
import pandas as pd
from services.repo_factory import get_repo
from services.notes_service import make_note, update_note_ts
from core.utils import parse_dt
from core.constants import RESULTADOS

st.set_page_config(page_title="Ata", page_icon="📝", layout="wide")
repo = get_repo()

st.title("📝 Ata / Relato da Visita")

clinics = repo.list_clinics()
visits = repo.list_visits()
if not visits:
    st.info("Nenhuma visita cadastrada ainda.")
    st.stop()

clin_by_id = {c['id']: c for c in clinics}

# Select visit: from session (when coming from Hoje) or via dropdown
preselected = st.session_state.pop('selected_visit_id', None)

options = []
for v in sorted(visits, key=lambda x: x.get('data_hora','')):
    c = clin_by_id.get(v.get('clinic_id'), {})
    dt = parse_dt(v.get('data_hora',''))
    label = f"{dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora','')} — {c.get('nome_cadastro','')} — {v.get('status','')}"
    options.append((label, v['id']))

labels = [x[0] for x in options]
id_by_label = {x[0]: x[1] for x in options}

idx = 0
if preselected:
    for i, (_, vid) in enumerate(options):
        if vid == preselected:
            idx = i
            break

visit_label = st.selectbox("Escolha a visita", options=labels, index=idx)
visit_id = id_by_label[visit_label]
visit = repo.get_visit(visit_id)

clinic = clin_by_id.get(visit.get('clinic_id'), {})

st.caption(f"Clínica: **{clinic.get('nome_cadastro','')}**")

# timeline
with st.expander("📚 Histórico recente da clínica", expanded=False):
    hist = [v for v in visits if v.get('clinic_id') == clinic.get('id')]
    hist = sorted(hist, key=lambda x: x.get('data_hora',''), reverse=True)[:10]
    hrows = []
    for h in hist:
        dt = parse_dt(h.get('data_hora',''))
        hrows.append({
            'data': dt.strftime('%d/%m/%Y %H:%M') if dt else h.get('data_hora',''),
            'status': h.get('status',''),
            'objetivo': h.get('objetivo','')
        })
    st.dataframe(pd.DataFrame(hrows), use_container_width=True, hide_index=True)

note = repo.get_note_by_visit(visit_id)
creating = False
if not note:
    note = make_note(visit_id)
    creating = True

with st.form("note_form"):
    col1, col2 = st.columns([1,1])
    with col1:
        resultado = st.selectbox("Resultado", options=[""] + RESULTADOS, index=([""]+RESULTADOS).index(note.get('resultado') if note.get('resultado') in RESULTADOS else ""))
    with col2:
        follow = st.date_input("Follow-up (se aplicável)", value=None)

    pauta = st.text_input("Pauta", value=note.get('pauta',''))
    tratado = st.text_area("O que foi tratado", value=note.get('o_que_foi_tratado',''), height=140)
    obj = st.text_area("Objeções", value=note.get('objecoes',''), height=90)
    acordos = st.text_area("Acordos / Compromissos", value=note.get('acordos',''), height=90)
    prox = st.text_area("Próximos passos", value=note.get('proximos_passos',''), height=110)

    save = st.form_submit_button("Salvar ata")

if save:
    note['resultado'] = resultado
    note['pauta'] = pauta
    note['o_que_foi_tratado'] = tratado
    note['objecoes'] = obj
    note['acordos'] = acordos
    note['proximos_passos'] = prox
    note['follow_up_data'] = follow.isoformat() if follow else ''
    update_note_ts(note, creating=creating)
    repo.upsert_note(note)
    st.success("Ata salva!")

st.divider()

c1, c2 = st.columns(2)
with c1:
    if st.button("✅ Marcar visita como realizada"):
        visit['status'] = 'REALIZADA'
        repo.upsert_visit(visit)
        st.success("Visita marcada como REALIZADA")
        st.rerun()
with c2:
    if st.button("↩️ Voltar para Hoje"):
        st.switch_page("pages/1_🏠_Hoje.py")
