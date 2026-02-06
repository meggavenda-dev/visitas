create extension if not exists pgcrypto;

create table if not exists clinics (
  id uuid primary key default gen_random_uuid(),
  id_origem bigint unique,
  nome_cadastro text not null,
  cidade text,
  uf text,
  telefone text,
  whatsapp text,
  email text,
  observacoes text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

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

create table if not exists visit_notes (
  id uuid primary key default gen_random_uuid(),
  visit_id uuid references visits(id) on delete cascade,
  resultado text,
  pauta text,
  o_que_foi_tratado text,
  acordos text,
  proximos_passos text,
  criado_em timestamptz default now(),
  atualizado_em timestamptz default now()
);

create unique index if not exists uq_note_visit on visit_notes(visit_id);

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
