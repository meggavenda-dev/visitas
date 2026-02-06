from __future__ import annotations
from core.utils import new_id, now_local

def make_note(visit_id: str):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'id': new_id(),
        'visit_id': visit_id,
        'resultado': '',
        'pauta': '',
        'o_que_foi_tratado': '',
        'objecoes': '',
        'acordos': '',
        'proximos_passos': '',
        'follow_up_data': '',
        'criado_em': now,
        'atualizado_em': now,
    }

def touch(note, creating=False):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not note.get('criado_em'):
        note['criado_em'] = now
    note['atualizado_em'] = now
    return note
