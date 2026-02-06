import streamlit as st
import pandas as pd
from services.repo_factory import get_repo
from services.clinics_service import make_empty_clinic, touch, import_clinics, next_manual_id
from core.constants import UF_LIST

st.set_page_config(page_title='Clínicas', page_icon='🏥', layout='wide')
repo = get_repo()

st.title('🏥 Clínicas (ID = IDCLINICA)')

with st.expander('📥 Importar Excel', expanded=False):
    st.caption('Aceita: aba "Clinicas" (modelo) ou planilha com colunas IDCLINICA e NomePJ.')
    up = st.file_uploader('Arquivo .xlsx', type=['xlsx'])
    if up is not None:
        try:
            xls = pd.ExcelFile(up)
            sheet = 'Clinicas' if 'Clinicas' in xls.sheet_names else xls.sheet_names[0]
            df = pd.read_excel(up, sheet_name=sheet)
            res = import_clinics(repo, df)
            st.success(f"Importação concluída: {res['created']} criadas, {res['updated']} atualizadas")
            st.rerun()
        except Exception as e:
            st.error(f"Falha ao importar: {e}")

st.divider()

clinics = sorted(repo.list_clinics(), key=lambda x: int(x.get('id')))
existing_ids = [int(c['id']) for c in clinics]

st.subheader('➕ Cadastrar / Editar')

sel_mode = st.radio('Modo', ['Cadastrar nova', 'Editar existente'], horizontal=True)

if sel_mode == 'Editar existente' and clinics:
    options = [f"{c.get('nome_cadastro','')} (ID {int(c['id'])})" for c in clinics]
    pick = st.selectbox('Escolha a clínica', options)
    clinic_id = int(pick.split('ID ')[1].replace(')',''))
    clinic = repo.get_clinic(clinic_id)
    creating = False
else:
    # cadastro novo
    creating = True
    suggested = next_manual_id(existing_ids)
    col_id, col_btn = st.columns([2,1])
    with col_id:
        clinic_id = st.number_input('ID da clínica (IDCLINICA)', min_value=1, value=int(suggested), step=1)
    with col_btn:
        if st.button('Gerar ID (9000000+)'):
            clinic_id = suggested
            st.session_state['new_clinic_id'] = int(clinic_id)
            st.rerun()

    clinic_id = int(st.session_state.get('new_clinic_id', clinic_id))
    clinic = make_empty_clinic(clinic_id, '')

# validação: se criando e ID já existe
if creating and repo.get_clinic(int(clinic.get('id'))):
    st.warning('Esse ID já existe. Escolha outro ID para cadastrar manualmente.')

with st.form('clinic_form'):
    # ID fixo
    st.text_input('ID', value=str(int(clinic.get('id'))), disabled=True)

    clinic['nome_cadastro'] = st.text_input('Nome (cadastro)', value=clinic.get('nome_cadastro',''))
    clinic['cidade'] = st.text_input('Cidade', value=clinic.get('cidade',''))
    clinic['uf'] = st.selectbox('UF', ['']+UF_LIST, index=(['']+UF_LIST).index(clinic.get('uf','') if clinic.get('uf','') in UF_LIST else ''))

    c1,c2,c3 = st.columns(3)
    clinic['telefone'] = c1.text_input('Telefone', value=clinic.get('telefone',''))
    clinic['whatsapp'] = c2.text_input('WhatsApp', value=clinic.get('whatsapp',''))
    clinic['email'] = c3.text_input('Email', value=clinic.get('email',''))

    clinic['observacoes'] = st.text_area('Observações', value=clinic.get('observacoes',''), height=120)

    save = st.form_submit_button('Salvar')

if save:
    # se criando, revalida id único
    if creating and repo.get_clinic(int(clinic.get('id'))):
        st.error('Não foi possível salvar: já existe uma clínica com esse ID.')
    elif not clinic.get('nome_cadastro'):
        st.error('Nome é obrigatório.')
    else:
        touch(clinic, creating=creating)
        repo.upsert_clinic(clinic)
        st.success('Clínica salva!')
        # limpar sugestão
        st.session_state.pop('new_clinic_id', None)
        st.rerun()

st.divider()
st.subheader('📋 Lista')
rows = [{
    'id': int(c.get('id')),
    'nome': c.get('nome_cadastro',''),
    'cidade': c.get('cidade',''),
    'uf': c.get('uf',''),
} for c in sorted(repo.list_clinics(), key=lambda x: int(x.get('id')))]

st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

if clinics:
    del_id = st.number_input('Excluir clínica (ID)', min_value=1, value=int(existing_ids[0]), step=1)
    if st.button('Excluir'):
        repo.delete_clinic(int(del_id))
        st.success('Excluída.')
        st.rerun()
