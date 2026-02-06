from __future__ import annotations
from core.utils import new_id, now_local

DEFAULT_FIELDS = {
    'nome_fantasia':'', 'cnpj':'',
    'endereco_logradouro':'','endereco_numero':'','endereco_complemento':'','bairro':'','cidade':'','uf':'','cep':'',
    'telefone':'','whatsapp':'','email':'','site':'',
    'especialidades':'','categoria':'','potencial':'','status':'ATIVA',
    'horario_preferido_visita':'','observacoes':'',
}

def make_clinic(id_origem, nome_cadastro: str):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    c = {'id': new_id(), 'id_origem': id_origem, 'nome_cadastro': nome_cadastro, 'created_at': now, 'updated_at': now}
    c.update(DEFAULT_FIELDS)
    return c

def touch(row, creating=False):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not row.get('created_at'):
        row['created_at'] = now
    row['updated_at'] = now
    return row

def import_clinics(repo, df):
    existing = repo.list_clinics()
    by_origem = {c.get('id_origem'): c for c in existing if c.get('id_origem') is not None}
    created=updated=0

    for _, r in df.iterrows():
        id_origem = r.get('id_origem', None)
        if id_origem is None:
            id_origem = r.get('id_clinica', None)
        nome = r.get('nome_cadastro', None) or r.get('nome_pj', None)
        if not nome:
            continue

        payload = dict(r)
        payload['nome_cadastro'] = str(nome).strip()
        if id_origem not in (None, ''):
            try:
                payload['id_origem'] = int(id_origem)
            except Exception:
                payload['id_origem'] = id_origem
        else:
            payload['id_origem'] = None

        if payload['id_origem'] is not None and payload['id_origem'] in by_origem:
            base = by_origem[payload['id_origem']]
            for k,v in payload.items():
                if k in base and v not in (None, ''):
                    base[k]=v
            touch(base)
            repo.upsert_clinic(base)
            updated += 1
        else:
            c = make_clinic(payload['id_origem'], payload['nome_cadastro'])
            for k,v in payload.items():
                if k in c and v not in (None, ''):
                    c[k]=v
            touch(c, creating=True)
            repo.upsert_clinic(c)
            created += 1

    return {'created': created, 'updated': updated}
