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

c1,c2,c3 = st.columns(3)
c1.metric("Hoje", len(today_list))
c2.metric("Próximos 7 dias", len(week_list))
c3.metric("Atrasadas", len(overdue))

st.divider()

clinic_filter = st.selectbox("Filtrar por clínica", ["Todas"] + sorted([c.get('nome_cadastro','') for c in clinics]))


def show(title, rows):
    st.subheader(title)
    for v in rows:
        c = clin_by_id.get(v.get('clinic_id'), {})
        if clinic_filter != 'Todas' and c.get('nome_cadastro') != clinic_filter:
            continue
        dt = parse_dt(v.get('data_hora',''))
        when = dt.strftime('%d/%m/%Y %H:%M') if dt else v.get('data_hora','')
        with st.container(border=True):
            a,b,cc,dd = st.columns([3,2,2,2])
            a.markdown(f"**{c.get('nome_cadastro','(sem clínica)')}**")
            b.write(when)
            cc.write(v.get('status',''))
            if dd.button("📝 Ata", key=f"ata_{v['id']}"):
                st.session_state['selected_visit_id'] = v['id']
                st.switch_page('pages/3_📝_Ata.py')

show("📌 Hoje", today_list)
st.divider()
show("📅 Semana", week_list)
st.divider()
show("⏰ Atrasadas", overdue)
