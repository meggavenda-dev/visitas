from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FILES = {
    "clinics": DATA_DIR / "clinics.json",
    "contacts": DATA_DIR / "contacts.json",
    "visits": DATA_DIR / "visits.json",
    "notes": DATA_DIR / "notes.json",
}

class LocalJsonRepo:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        for p in FILES.values():
            if not p.exists():
                p.write_text("[]", encoding="utf-8")

    def _read(self, key: str) -> List[Dict[str, Any]]:
        return json.loads(FILES[key].read_text(encoding="utf-8"))

    def _write(self, key: str, rows: List[Dict[str, Any]]):
        FILES[key].write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_clinics(self):
        return self._read('clinics')

    def get_clinic(self, clinic_id: str):
        return next((c for c in self._read('clinics') if c.get('id') == clinic_id), None)

    def upsert_clinic(self, clinic: Dict[str, Any]):
        rows = self._read('clinics')
        idx = next((i for i, c in enumerate(rows) if c.get('id') == clinic.get('id')), None)
        if idx is None:
            rows.append(clinic)
        else:
            rows[idx] = clinic
        self._write('clinics', rows)
        return clinic

    def delete_clinic(self, clinic_id: str):
        self._write('clinics', [c for c in self._read('clinics') if c.get('id') != clinic_id])
        self._write('contacts', [c for c in self._read('contacts') if c.get('clinic_id') != clinic_id])
        visits = [v for v in self._read('visits') if v.get('clinic_id') != clinic_id]
        self._write('visits', visits)
        keep_visit_ids = {v.get('id') for v in visits}
        self._write('notes', [n for n in self._read('notes') if n.get('visit_id') in keep_visit_ids])

    def list_contacts(self, clinic_id: str):
        return [c for c in self._read('contacts') if c.get('clinic_id') == clinic_id]

    def upsert_contact(self, contact: Dict[str, Any]):
        rows = self._read('contacts')
        idx = next((i for i, c in enumerate(rows) if c.get('id') == contact.get('id')), None)
        if idx is None:
            rows.append(contact)
        else:
            rows[idx] = contact
        self._write('contacts', rows)
        return contact

    def delete_contact(self, contact_id: str):
        self._write('contacts', [c for c in self._read('contacts') if c.get('id') != contact_id])

    def list_visits(self):
        return self._read('visits')

    def get_visit(self, visit_id: str):
        return next((v for v in self._read('visits') if v.get('id') == visit_id), None)

    def upsert_visit(self, visit: Dict[str, Any]):
        rows = self._read('visits')
        idx = next((i for i, v in enumerate(rows) if v.get('id') == visit.get('id')), None)
        if idx is None:
            rows.append(visit)
        else:
            rows[idx] = visit
        self._write('visits', rows)
        return visit

    def delete_visit(self, visit_id: str):
        self._write('visits', [v for v in self._read('visits') if v.get('id') != visit_id])
        self._write('notes', [n for n in self._read('notes') if n.get('visit_id') != visit_id])

    def get_note_by_visit(self, visit_id: str):
        return next((n for n in self._read('notes') if n.get('visit_id') == visit_id), None)

    def upsert_note(self, note: Dict[str, Any]):
        rows = self._read('notes')
        idx = next((i for i, n in enumerate(rows) if n.get('id') == note.get('id')), None)
        if idx is None:
            rows.append(note)
        else:
            rows[idx] = note
        self._write('notes', rows)
        return note
