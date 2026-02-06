from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class Clinic(BaseModel):
    id: str
    id_origem: Optional[int] = None
    nome_cadastro: str
    nome_fantasia: str = ""
    cnpj: str = ""

    endereco_logradouro: str = ""
    endereco_numero: str = ""
    endereco_complemento: str = ""
    bairro: str = ""
    cidade: str = ""
    uf: str = ""
    cep: str = ""

    telefone: str = ""
    whatsapp: str = ""
    email: str = ""
    site: str = ""

    especialidades: str = ""
    categoria: str = ""
    potencial: str = ""
    status: str = "ATIVA"

    horario_preferido_visita: str = ""
    observacoes: str = ""

    created_at: str = ""
    updated_at: str = ""

class Contact(BaseModel):
    id: str
    clinic_id: str
    nome: str
    cargo: str = ""
    telefone: str = ""
    whatsapp: str = ""
    email: str = ""
    observacoes: str = ""
    principal: bool = False

class Visit(BaseModel):
    id: str
    clinic_id: str
    data_hora: str  # ISO format
    status: str = "AGENDADA"
    objetivo: str = ""
    assuntos: str = ""
    criado_em: str = ""
    atualizado_em: str = ""

class VisitNote(BaseModel):
    id: str
    visit_id: str
    resultado: str = ""
    pauta: str = ""
    o_que_foi_tratado: str = ""
    objecoes: str = ""
    acordos: str = ""
    proximos_passos: str = ""
    follow_up_data: str = ""  # YYYY-MM-DD
    criado_em: str = ""
    atualizado_em: str = ""
