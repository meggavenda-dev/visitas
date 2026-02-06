from __future__ import annotations
from typing import Dict, Any, List
from core.utils import new_id, now_local

DEFAULT_FIELDS = {
    'nome_fantasia':'', 'cnpj':'',
    'endereco_logradouro':'','endereco_numero':'','endereco_complemento':'','bairro':'','cidade':'','uf':'','cep':'',
    'telefone':'','whatsapp':'','email':'','site':'',
    'especialidades':'','categoria':'','potencial':'','status':'ATIVA',
    'horario_preferido_visita':'','observacoes':'',
}


def make_clinic_from_origem(id_origem: int | None, nome: str) -> Dict[str, Any]:
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    clinic = {
        'id': new_id(),
        'id_origem': id_origem,
        'nome_cadastro': nome,
        'created_at': now,
        'updated_at': now,
    }
    clinic.update(DEFAULT_FIELDS)
    return clinic


def update_timestamps(row: Dict[str, Any], creating: bool=False) -> Dict[str, Any]:
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not row.get('created_at'):
        row['created_at'] = now
    row['updated_at'] = now
    return row


def import_clinics_from_dataframe(repo, df) -> Dict[str, int]:
    """Importa/atualiza clínicas.

    Espera colunas mínimas: id_clinica (ou id_origem) e nome_cadastro (ou nome_pj/nome).
    Se existir coluna 'id' (uuid) no arquivo, respeita.

    Regra:
    - Se 'id' existir e bater com um registro -> atualiza.
    - Senão, se 'id_origem' existir e já tiver no banco -> atualiza aquele.
    - Senão cria novo.
    """
    existing = repo.list_clinics()
    by_id = {c.get('id'): c for c in existing}
    by_origem = {c.get('id_origem'): c for c in existing if c.get('id_origem') is not None}

    created = 0
    updated = 0

    for _, r in df.iterrows():
        rid = r.get('id', None)
        id_origem = r.get('id_origem', None)
        if id_origem is None:
            id_origem = r.get('id_clinica', None)
        nome = r.get('nome_cadastro', None)
        if nome is None:
            nome = r.get('nome_pj', None)
        if nome is None:
            nome = r.get('nome', None)
        if nome is None:
            continue

        payload = dict(r)
        payload['id_origem'] = int(id_origem) if id_origem not in (None, '') and str(id_origem).isdigit() else (id_origem if id_origem not in ('',) else None)
        payload['nome_cadastro'] = str(nome).strip()

        if rid and rid in by_id:
            base = by_id[rid]
            base.update({k: v for k, v in payload.items() if k})
            update_timestamps(base)
            repo.upsert_clinic(base)
            updated += 1
            continue

        if payload.get('id_origem') is not None and payload.get('id_origem') in by_origem:
            base = by_origem[payload.get('id_origem')]
            base.update({k: v for k, v in payload.items() if k})
            update_timestamps(base)
            repo.upsert_clinic(base)
            updated += 1
            continue

        newc = make_clinic_from_origem(payload.get('id_origem'), payload.get('nome_cadastro'))
        # bring optional cols
        for k, v in payload.items():
            if k in newc:
                newc[k] = v
        update_timestamps(newc, creating=True)
        repo.upsert_clinic(newc)
        created += 1

    return {'created': created, 'updated': updated}
