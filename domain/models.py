from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Clinic:
    id: str
    id_origem: Optional[int] = None
    nome_cadastro: str = ''

@dataclass
class Visit:
    id: str
    clinic_id: str
    data_hora: str
    status: str = 'AGENDADA'
