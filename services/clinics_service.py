from __future__ import annotations
import pandas as pd
from core.utils import now_local
from core.constants import MANUAL_ID_MIN

DEFAULT_FIELDS = {
    'nome_fantasia':'', 'cnpj':'',
    'endereco_logradouro':'','endereco_numero':'','endereco_complemento':'','bairro':'','cidade':'','uf':'','cep':'',
    'telefone':'','whatsapp':'','email':'','site':'',
    'especialidades':'','categoria':'','potencial':'','status':'ATIVA',
    'horario_preferido_visita':'','observacoes':'',
}

def touch(row, creating=False):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not row.get('created_at'):
        row['created_at'] = now
    row['updated_at'] = now
    return row

def next_manual_id(existing_ids: list[int]) -> int:
    mx = max(existing_ids) if existing_ids else 0
    return max(MANUAL_ID_MIN, mx + 1)

def make_empty_clinic(clinic_id: int, nome_cadastro: str):
    c = {'id': int(clinic_id), 'nome_cadastro': nome_cadastro}
    c.update(DEFAULT_FIELDS)
    touch(c, creating=True)
    return c

def normalize_import_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    # map possible names
    rename = {}
    if 'idclinica' in df.columns: rename['idclinica'] = 'id'
    if 'id_clinica' in df.columns: rename['id_clinica'] = 'id'
    if 'id' not in df.columns and 'id_origem' in df.columns: rename['id_origem'] = 'id'
    if 'nomepj' in df.columns: rename['nomepj'] = 'nome_cadastro'
    if 'nome_pj' in df.columns: rename['nome_pj'] = 'nome_cadastro'
    df = df.rename(columns=rename)
    if 'id' in df.columns:
        df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    if 'nome_cadastro' in df.columns:
        df['nome_cadastro'] = df['nome_cadastro'].astype(str).str.strip()
    return df

def import_clinics(repo, df: pd.DataFrame):
    df = normalize_import_df(df)
    existing = repo.list_clinics()
    by_id = {int(c['id']): c for c in existing}

    created = 0
    updated = 0

    for _, r in df.iterrows():
        cid = r.get('id', None)
        nome = r.get('nome_cadastro', None)
        if pd.isna(cid) or not nome:
            continue
        cid = int(cid)
        payload = dict(r)
        payload['id'] = cid
        payload['nome_cadastro'] = str(nome).strip()

        if cid in by_id:
            base = by_id[cid]
            for k, v in payload.items():
                if k in base and v not in (None, '') and not (isinstance(v, float) and pd.isna(v)):
                    base[k] = v
            touch(base)
            repo.upsert_clinic(base)
            updated += 1
        else:
            c = make_empty_clinic(cid, payload['nome_cadastro'])
            for k, v in payload.items():
                if k in c and v not in (None, '') and not (isinstance(v, float) and pd.isna(v)):
                    c[k] = v
            touch(c, creating=True)
            repo.upsert_clinic(c)
            created += 1

    return {'created': created, 'updated': updated}
