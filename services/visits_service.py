from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime, timedelta
from core.utils import new_id, now_local, today_local, parse_dt
from core.constants import VisitStatus


def make_visit(clinic_id: str, data_hora: datetime, objetivo: str, assuntos: str) -> Dict[str, Any]:
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'id': new_id(),
        'clinic_id': clinic_id,
        'data_hora': data_hora.isoformat(timespec='minutes'),
        'status': VisitStatus.AGENDADA.value,
        'objetivo': objetivo or '',
        'assuntos': assuntos or '',
        'criado_em': now,
        'atualizado_em': now,
    }


def update_visit_ts(visit: Dict[str, Any], creating: bool=False) -> Dict[str, Any]:
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not visit.get('criado_em'):
        visit['criado_em'] = now
    visit['atualizado_em'] = now
    return visit


def categorize_visits(visits: List[Dict[str, Any]]):
    today = today_local()
    now = now_local()

    def v_dt(v):
        dt = parse_dt(v.get('data_hora',''))
        return dt or datetime.max

    visits_sorted = sorted(visits, key=v_dt)

    today_list = []
    week_list = []
    overdue = []

    for v in visits_sorted:
        dt = parse_dt(v.get('data_hora',''))
        if not dt:
            continue
        d = dt.date()
        if v.get('status') == VisitStatus.REALIZADA.value or v.get('status') == VisitStatus.CANCELADA.value:
            continue
        if d == today:
            today_list.append(v)
        elif today < d <= (today + timedelta(days=7)):
            week_list.append(v)
        elif dt < now:
            overdue.append(v)

    return today_list, week_list, overdue
