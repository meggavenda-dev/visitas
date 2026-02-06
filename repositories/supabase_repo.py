from __future__ import annotations
from supabase import create_client

class SupabaseRepo:
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)

    def list_clinics(self):
        return self.client.table('clinics').select('*').order('nome_cadastro').execute().data

    def get_clinic(self, clinic_id: str):
        data = self.client.table('clinics').select('*').eq('id', clinic_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_clinic(self, clinic):
        data = self.client.table('clinics').upsert(clinic).execute().data
        return data[0] if data else clinic

    def delete_clinic(self, clinic_id: str):
        self.client.table('clinics').delete().eq('id', clinic_id).execute()

    def list_contacts(self, clinic_id: str):
        return self.client.table('contacts').select('*').eq('clinic_id', clinic_id).execute().data

    def upsert_contact(self, contact):
        data = self.client.table('contacts').upsert(contact).execute().data
        return data[0] if data else contact

    def delete_contact(self, contact_id: str):
        self.client.table('contacts').delete().eq('id', contact_id).execute()

    def list_visits(self):
        return self.client.table('visits').select('*').order('data_hora').execute().data

    def get_visit(self, visit_id: str):
        data = self.client.table('visits').select('*').eq('id', visit_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_visit(self, visit):
        data = self.client.table('visits').upsert(visit).execute().data
        return data[0] if data else visit

    def delete_visit(self, visit_id: str):
        self.client.table('visits').delete().eq('id', visit_id).execute()

    def get_note_by_visit(self, visit_id: str):
        data = self.client.table('visit_notes').select('*').eq('visit_id', visit_id).limit(1).execute().data
        return data[0] if data else None

    def upsert_note(self, note):
        data = self.client.table('visit_notes').upsert(note).execute().data
        return data[0] if data else note
