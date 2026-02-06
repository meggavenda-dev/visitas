from __future__ import annotations
from typing import Dict, Any
from core.utils import new_id, now_local


def make_note(visit_id: str) -> Dict[str, Any]:
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


def update_note_ts(note: Dict[str, Any], creating: bool=False) -> Dict[str, Any]:
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not note.get('criado_em'):
        note['criado_em'] = now
    note['atualizado_em'] = now
    return note
