import streamlit as st
import pandas as pd
from services.repo_factory import get_repo
from services.clinics_service import make_clinic_from_origem, update_timestamps, import_clinics_from_dataframe
from core.utils import new_id
from core.constants import UF_LIST

st.set_page_config(page_title="Clínicas", page_icon="🏥", layout="wide")
repo = get_repo()

st.title("🏥 Clínicas")

# Import
with st.expander("📥 Importar clínicas (Excel)", expanded=False):
    st.markdown("- Faça upload de um Excel com aba **Clinicas** (recomendado) ou uma planilha com colunas `id_clinica` e `nome_pj`.
- Se a aba **Clinicas** tiver as colunas extras, elas são importadas também.")
    up = st.file_uploader("Arquivo .xlsx", type=['xlsx'])
    if up is not None:
        try:
            xls = pd.ExcelFile(up)
            sheet = 'Clinicas' if 'Clinicas' in xls.sheet_names else xls.sheet_names[0]
            df = pd.read_excel(up, sheet_name=sheet)
            # normalize
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename = {}
            if 'idclinica' in df.columns: rename['idclinica'] = 'id_clinica'
            if 'nomepj' in df.columns: rename['nomepj'] = 'nome_pj'
            df = df.rename(columns=rename)

            res = import_clinics_from_dataframe(repo, df)
            st.success(f"Importação concluída: {res['created']} criadas, {res['updated']} atualizadas.")
            st.rerun()
        except Exception as e:
            st.error(f"Falha ao importar: {e}")

st.divider()

clinics = repo.list_clinics()
clinics = sorted(clinics, key=lambda x: x.get('nome_cadastro',''))

# Cadastro/edição
st.subheader("➕ Cadastrar / Editar clínica")

sel = st.selectbox("Selecionar clínica para editar", options=["(Nova)"] + [c['nome_cadastro'] for c in clinics])
clinic = None
creating = False
if sel == "(Nova)":
    creating = True
    clinic = make_clinic_from_origem(None, "")
else:
    clinic = next(c for c in clinics if c['nome_cadastro'] == sel)

with st.form("clinic_form"):
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        clinic['nome_cadastro'] = st.text_input("Nome (cadastro)", value=clinic.get('nome_cadastro',''))
    with col2:
        clinic['status'] = st.selectbox("Status", options=["ATIVA","INATIVA"], index=(0 if clinic.get('status','ATIVA')=='ATIVA' else 1))
    with col3:
        clinic['potencial'] = st.selectbox("Potencial", options=["","Alto","Médio","Baixo"], index=["","Alto","Médio","Baixo"].index(clinic.get('potencial','') if clinic.get('potencial','') in ["","Alto","Médio","Baixo"] else ""))

    clinic['nome_fantasia'] = st.text_input("Nome fantasia", value=clinic.get('nome_fantasia',''))
    clinic['cnpj'] = st.text_input("CNPJ", value=clinic.get('cnpj',''))

    st.markdown("**Endereço**")
    a1, a2, a3 = st.columns([3,1,2])
    clinic['endereco_logradouro'] = a1.text_input("Logradouro", value=clinic.get('endereco_logradouro',''))
    clinic['endereco_numero'] = a2.text_input("Nº", value=clinic.get('endereco_numero',''))
    clinic['endereco_complemento'] = a3.text_input("Complemento", value=clinic.get('endereco_complemento',''))

    b1, b2, b3, b4 = st.columns([2,2,1,1])
    clinic['bairro'] = b1.text_input("Bairro", value=clinic.get('bairro',''))
    clinic['cidade'] = b2.text_input("Cidade", value=clinic.get('cidade',''))
    clinic['uf'] = b3.selectbox("UF", options=[""] + UF_LIST, index=([""]+UF_LIST).index(clinic.get('uf','') if clinic.get('uf','') in UF_LIST else ""))
    clinic['cep'] = b4.text_input("CEP", value=clinic.get('cep',''))

    st.markdown("**Contato**")
    c1, c2, c3, c4 = st.columns(4)
    clinic['telefone'] = c1.text_input("Telefone", value=clinic.get('telefone',''))
    clinic['whatsapp'] = c2.text_input("WhatsApp", value=clinic.get('whatsapp',''))
    clinic['email'] = c3.text_input("Email", value=clinic.get('email',''))
    clinic['site'] = c4.text_input("Site", value=clinic.get('site',''))

    clinic['especialidades'] = st.text_input("Especialidades (tags)", value=clinic.get('especialidades',''))
    clinic['categoria'] = st.text_input("Categoria (A/B/C)", value=clinic.get('categoria',''))
    clinic['horario_preferido_visita'] = st.text_input("Horário preferido para visita", value=clinic.get('horario_preferido_visita',''))
    clinic['observacoes'] = st.text_area("Observações", value=clinic.get('observacoes',''), height=120)

    save = st.form_submit_button("Salvar clínica")

if save:
    if not clinic.get('nome_cadastro'):
        st.error("O nome da clínica é obrigatório.")
    else:
        update_timestamps(clinic, creating=creating)
        repo.upsert_clinic(clinic)
        st.success("Clínica salva!")
        st.rerun()

st.divider()

# Listagem
st.subheader("📋 Lista de clínicas")

rows = []
for c in clinics:
    rows.append({
        'id': c.get('id'),
        'id_origem': c.get('id_origem'),
        'nome': c.get('nome_cadastro'),
        'cidade': c.get('cidade',''),
        'uf': c.get('uf',''),
        'status': c.get('status',''),
        'potencial': c.get('potencial','')
    })

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

colA, colB = st.columns([2,3])
with colA:
    pick = st.selectbox("Selecionar clínica (por ID)", options=[""] + list(df['id']) if not df.empty else [""])
with colB:
    if st.button("Excluir clínica") and pick:
        repo.delete_clinic(pick)
        st.success("Clínica excluída.")
        st.rerun()

# Contacts management (simple)
st.divider()
st.subheader("👥 Contatos da clínica")

pick_clinic = st.selectbox("Escolha uma clínica para ver/editar contatos", options=["(Selecione)"] + [c['nome_cadastro'] for c in clinics])
if pick_clinic != "(Selecione)":
    cl = next(c for c in clinics if c['nome_cadastro'] == pick_clinic)
    contacts = repo.list_contacts(cl['id'])

    st.caption(f"Clínica: **{cl['nome_cadastro']}**")

    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome")
        cargo = col2.text_input("Cargo")
        col3, col4, col5 = st.columns(3)
        tel = col3.text_input("Telefone")
        wpp = col4.text_input("WhatsApp")
        email = col5.text_input("Email")
        obs = st.text_area("Observações", height=80)
        principal = st.checkbox("Contato principal", value=False)
        add = st.form_submit_button("Adicionar contato")

    if add:
        contact = {
            'id': new_id(),
            'clinic_id': cl['id'],
            'nome': nome,
            'cargo': cargo,
            'telefone': tel,
            'whatsapp': wpp,
            'email': email,
            'observacoes': obs,
            'principal': principal,
        }
        repo.upsert_contact(contact)
        st.success("Contato adicionado!")
        st.rerun()

    if contacts:
        cdf = pd.DataFrame([{k: v for k, v in c.items() if k in ['id','nome','cargo','telefone','whatsapp','email','principal']} for c in contacts])
        st.dataframe(cdf, use_container_width=True, hide_index=True)

        del_id = st.selectbox("Excluir contato (ID)", options=[""] + list(cdf['id']))
        if st.button("Excluir contato") and del_id:
            repo.delete_contact(del_id)
            st.success("Contato excluído.")
            st.rerun()
    else:
        st.caption("Sem contatos cadastrados para esta clínica.")
