from __future__ import annotations
from typing import List, Dict, Any, Optional
from supabase import create_client, Client

class SupabaseRepo:
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    # Clinics
    def list_clinics(self) -> List[Dict[str, Any]]:
        return self.client.table('clinics').select('*').order('nome_cadastro').execute().data

    def get_clinic(self, clinic_id: str) -> Optional[Dict[str, Any]]:
        data = self.client.table('clinics').select('*').eq('id', clinic_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_clinic(self, clinic: Dict[str, Any]) -> Dict[str, Any]:
        # upsert by id (or id_origem if you prefer)
        data = self.client.table('clinics').upsert(clinic).execute().data
        return data[0] if data else clinic

    def delete_clinic(self, clinic_id: str) -> None:
        self.client.table('clinics').delete().eq('id', clinic_id).execute()

    # Contacts
    def list_contacts(self, clinic_id: str) -> List[Dict[str, Any]]:
        return self.client.table('contacts').select('*').eq('clinic_id', clinic_id).order('principal', desc=True).execute().data

    def upsert_contact(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        data = self.client.table('contacts').upsert(contact).execute().data
        return data[0] if data else contact

    def delete_contact(self, contact_id: str) -> None:
        self.client.table('contacts').delete().eq('id', contact_id).execute()

    # Visits
    def list_visits(self) -> List[Dict[str, Any]]:
        return self.client.table('visits').select('*').order('data_hora').execute().data

    def get_visit(self, visit_id: str) -> Optional[Dict[str, Any]]:
        data = self.client.table('visits').select('*').eq('id', visit_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_visit(self, visit: Dict[str, Any]) -> Dict[str, Any]:
        data = self.client.table('visits').upsert(visit).execute().data
        return data[0] if data else visit

    def delete_visit(self, visit_id: str) -> None:
        self.client.table('visits').delete().eq('id', visit_id).execute()

    # Notes
    def get_note_by_visit(self, visit_id: str) -> Optional[Dict[str, Any]]:
        data = self.client.table('visit_notes').select('*').eq('visit_id', visit_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_note(self, note: Dict[str, Any]) -> Dict[str, Any]:
        data = self.client.table('visit_notes').upsert(note).execute().data
        return data[0] if data else note
