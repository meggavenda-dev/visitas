from __future__ import annotations
from datetime import datetime, date, timedelta
from dateutil import tz
import uuid

def now_local() -> datetime:
    return datetime.now(tz=tz.tzlocal())

def today_local() -> date:
    return now_local().date()

def new_id() -> str:
    return str(uuid.uuid4())

def parse_dt(dt_str: str):
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None
