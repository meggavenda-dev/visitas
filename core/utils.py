from __future__ import annotations
from datetime import datetime, date, timedelta
from dateutil import tz
import uuid

def now_local() -> datetime:
    # Usa timezone local do servidor (Streamlit Cloud pode ser UTC). No mobile/web você ajusta.
    return datetime.now(tz=tz.tzlocal())

def today_local() -> date:
    return now_local().date()

def in_next_days(d: date, days: int = 7) -> bool:
    t = today_local()
    return t <= d <= (t + timedelta(days=days))

def new_id() -> str:
    return str(uuid.uuid4())

def safe_str(x) -> str:
    return "" if x is None else str(x).strip()

def parse_dt(dt_str: str) -> datetime | None:
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None
