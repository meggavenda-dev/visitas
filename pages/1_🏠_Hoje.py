import streamlit as st
from services.repo_factory import get_repo
from services.visits_service import categorize_visits
from core.utils import parse_dt

st.set_page_config(page_title="Hoje", page_icon="🏠", layout="wide")

repo = get_repo()

st.title("🏠 Hoje")

clinics = repo.list_clinics()
clin_by_id = {c['id']: c for c in clinics}
visits = repo.list_visits()

today_list, week_list, overdue = categorize_visits(visits)

c1, c2, c3 = st.columns(3)
c1.metric("Hoje", len(today_list))
c2.metric("Próximos 7 dias", len(week_list))
c3.metric("Atrasadas", len(overdue))

st.divider()

fcol1, fcol2, fcol3 = st.columns([2,1,1])
with fcol1:
    clinic_filter = st.selectbox("Filtrar por clínica", ["Todas"] + sorted([c['nome_cadastro'] for c in clinics]))
with fcol2:
    status_filter = st.selectbox("Status", ["Todos", "AGENDADA", "REMARCADA", "CANCELADA", "REALIZADA"], index=0)
with fcol3:
    show_overdue = st.checkbox("Mostrar atrasadas", value=True)


def apply_filters(rows):
    out = []
    for v in rows:
        c = clin_by_id.get(v.get('clinic_id'))
        if clinic_filter != "Todas" and c and c.get('nome_cadastro') != clinic_filter:
            continue
        if status_filter != "Todos" and v.get('status') != status_filter:
            continue
        out.append(v)
    return out


def render_list(title, rows):
    st.subheader(title)
    rows = apply_filters(rows)
    if not rows:
        st.caption("Nada por aqui.")
        return

    for v in rows:
        c = clin_by_id.get(v.get('clinic_id'), {})
        dt = parse_dt(v.get('data_hora',''))
        when = dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora','')
        with st.container(border=True):
            top1, top2, top3, top4 = st.columns([3,2,2,2])
            top1.markdown(f"**{c.get('nome_cadastro','(sem clínica)')}**")
            top2.write(when)
            top3.write(v.get('status',''))
            if top4.button("📝 Registrar ata", key=f"ata_{v['id']}"):
                st.session_state['selected_visit_id'] = v['id']
                st.switch_page("pages/3_📝_Ata_da_Visita.py")

            b1, b2, b3, b4 = st.columns([1,1,1,3])
            if b1.button("✅ Realizada", key=f"done_{v['id']}"):
                v['status'] = 'REALIZADA'
                repo.upsert_visit(v)
                st.rerun()
            if b2.button("↪️ Remarcar", key=f"resch_{v['id']}"):
                st.session_state['edit_visit_id'] = v['id']
                st.switch_page("pages/2_📅_Agendar.py")
            if b3.button("❌ Cancelar", key=f"cancel_{v['id']}"):
                v['status'] = 'CANCELADA'
                repo.upsert_visit(v)
                st.rerun()
            b4.caption(v.get('objetivo',''))


render_list("📌 Visitas de hoje", today_list)

st.divider()
render_list("📅 Visitas da semana (próximos 7 dias)", week_list)

if show_overdue:
    st.divider()
    render_list("⏰ Atrasadas", overdue)
