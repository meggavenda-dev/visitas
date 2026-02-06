from core.config import get_backend, get_supabase_key, get_supabase_url
from repositories.local_json_repo import LocalJsonRepo
from repositories.supabase_repo import SupabaseRepo

def get_repo():
    backend = get_backend().lower()
    if backend == 'supabase':
        url = get_supabase_url()
        key = get_supabase_key()
        if url and key:
            return SupabaseRepo(url, key)
    return LocalJsonRepo()
