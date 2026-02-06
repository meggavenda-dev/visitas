import streamlit as st
import pandas as pd
from services.repo_factory import get_repo
from services.clinics_service import make_clinic, touch, import_clinics
from core.utils import new_id
from core.constants import UF_LIST

st.set_page_config(page_title='Clínicas', page_icon='🏥', layout='wide')
repo = get_repo()

st.title('🏥 Clínicas')

with st.expander('📥 Importar Excel', expanded=False):
    up = st.file_uploader('Arquivo .xlsx', type=['xlsx'])
    if up is not None:
        xls = pd.ExcelFile(up)
        sheet = 'Clinicas' if 'Clinicas' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(up, sheet_name=sheet)
        df.columns = [str(c).strip().lower() for c in df.columns]
        rename = {}
        if 'idclinica' in df.columns: rename['idclinica']='id_origem'
        if 'nomepj' in df.columns: rename['nomepj']='nome_cadastro'
        if 'id_clinica' in df.columns: rename['id_clinica']='id_origem'
        df = df.rename(columns=rename)
        res = import_clinics(repo, df)
        st.success(f"Importado: {res['created']} criadas, {res['updated']} atualizadas")
        st.rerun()

st.divider()

clinics = sorted(repo.list_clinics(), key=lambda x: x.get('nome_cadastro',''))

sel = st.selectbox('Editar clínica', ['(Nova)'] + [c.get('nome_cadastro','') for c in clinics])
creating = sel=='(Nova)'
clinic = make_clinic(None, '') if creating else next(c for c in clinics if c.get('nome_cadastro')==sel)

with st.form('clinic_form'):
    clinic['nome_cadastro'] = st.text_input('Nome', value=clinic.get('nome_cadastro',''))
    clinic['cidade'] = st.text_input('Cidade', value=clinic.get('cidade',''))
    clinic['uf'] = st.selectbox('UF', ['']+UF_LIST, index=(['']+UF_LIST).index(clinic.get('uf','') if clinic.get('uf','') in UF_LIST else ''))
    clinic['telefone'] = st.text_input('Telefone', value=clinic.get('telefone',''))
    clinic['whatsapp'] = st.text_input('WhatsApp', value=clinic.get('whatsapp',''))
    clinic['email'] = st.text_input('Email', value=clinic.get('email',''))
    clinic['observacoes'] = st.text_area('Observações', value=clinic.get('observacoes',''), height=120)
    save = st.form_submit_button('Salvar')

if save:
    if not clinic.get('nome_cadastro'):
        st.error('Nome é obrigatório')
    else:
        touch(clinic, creating=creating)
        repo.upsert_clinic(clinic)
        st.success('Salvo!')
        st.rerun()

st.divider()
rows=[{'id': c.get('id'), 'id_origem': c.get('id_origem'), 'nome': c.get('nome_cadastro'), 'cidade': c.get('cidade',''), 'uf': c.get('uf','')} for c in clinics]
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
