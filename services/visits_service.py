from __future__ import annotations
from datetime import datetime, timedelta
from core.utils import new_id, now_local, today_local, parse_dt
from core.constants import VisitStatus


def make_visit(clinic_id: str, data_hora: datetime, objetivo: str, assuntos: str, status: str):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'id': new_id(),
        'clinic_id': clinic_id,
        'data_hora': data_hora.isoformat(timespec='minutes'),
        'status': status or VisitStatus.AGENDADA.value,
        'objetivo': objetivo or '',
        'assuntos': assuntos or '',
        'criado_em': now,
        'atualizado_em': now,
    }


def touch(visit, creating=False):
    now = now_local().strftime('%Y-%m-%d %H:%M:%S')
    if creating and not visit.get('criado_em'):
        visit['criado_em'] = now
    visit['atualizado_em'] = now
    return visit


def categorize_visits(visits):
    today = today_local()
    now = now_local()

    def v_dt(v):
        dt = parse_dt(v.get('data_hora',''))
        return dt or datetime.max

    visits_sorted = sorted(visits, key=v_dt)
    today_list=[]; week_list=[]; overdue=[]

    for v in visits_sorted:
        dt = parse_dt(v.get('data_hora',''))
        if not dt:
            continue
        if v.get('status') in (VisitStatus.REALIZADA.value, VisitStatus.CANCELADA.value):
            continue
        d = dt.date()
        if d == today:
            today_list.append(v)
        elif today < d <= (today + timedelta(days=7)):
            week_list.append(v)
        elif dt < now:
            overdue.append(v)

    return today_list, week_list, overdue
