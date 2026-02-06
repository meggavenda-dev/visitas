from __future__ import annotations
from datetime import datetime, date
import uuid

def now_local() -> datetime:
    # Streamlit Cloud normalmente roda em UTC.
    # Para app (mobile) você ajusta fuso depois; aqui mantemos estável.
    return datetime.utcnow()

def today_local() -> date:
    return now_local().date()

def new_uuid() -> str:
    return str(uuid.uuid4())

def parse_dt(dt_str: str):
    if not dt_str:
        return None
    try:
        # Aceita ISO com ou sem segundos
        return datetime.fromisoformat(dt_str)
    except Exception:
        return None
