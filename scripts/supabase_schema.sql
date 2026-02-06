-- Schema inicial para Supabase (Postgres)
-- Rode no SQL Editor do Supabase.

create extension if not exists pgcrypto;

create table if not exists clinics (
  id uuid primary key default gen_random_uuid(),
  id_origem bigint unique,
  nome_cadastro text not null,
  nome_fantasia text,
  cnpj text,

  endereco_logradouro text,
  endereco_numero text,
  endereco_complemento text,
  bairro text,
  cidade text,
  uf text,
  cep text,

  telefone text,
  whatsapp text,
  email text,
  site text,

  especialidades text,
  categoria text,
  potencial text,
  status text default 'ATIVA',
  horario_preferido_visita text,
  observacoes text,

  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists contacts (
  id uuid primary key default gen_random_uuid(),
  clinic_id uuid references clinics(id) on delete cascade,
  nome text not null,
  cargo text,
  telefone text,
  whatsapp text,
  email text,
  observacoes text,
  principal boolean default false,
  created_at timestamptz default now()
);

create index if not exists idx_contacts_clinic on contacts(clinic_id);

create table if not exists visits (
  id uuid primary key default gen_random_uuid(),
  clinic_id uuid references clinics(id) on delete cascade,
  data_hora timestamptz not null,
  status text default 'AGENDADA',
  objetivo text,
  assuntos text,
  criado_em timestamptz default now(),
  atualizado_em timestamptz default now()
);

create index if not exists idx_visits_date on visits(data_hora);

create table if not exists visit_notes (
  id uuid primary key default gen_random_uuid(),
  visit_id uuid references visits(id) on delete cascade,
  resultado text,
  pauta text,
  o_que_foi_tratado text,
  objecoes text,
  acordos text,
  proximos_passos text,
  follow_up_data date,
  criado_em timestamptz default now(),
  atualizado_em timestamptz default now()
);

create unique index if not exists uq_note_visit on visit_notes(visit_id);
