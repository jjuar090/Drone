-- Orders table for drone delivery: stores order details and delivery coordinates.
-- Run this in the Supabase SQL Editor (Dashboard -> SQL Editor).

create table if not exists public.orders (
  id uuid not null default gen_random_uuid(),
  created_at timestamptz null default now(),
  items jsonb not null,
  total numeric not null,
  latitude numeric not null,
  longitude numeric not null,
  accuracy numeric null default 0,
  constraint orders_pkey primary key (id)
) tablespace pg_default;

comment on table public.orders is 'Orders with delivery coordinates for drone missions.';
comment on column public.orders.items is 'Order line items (JSON).';
comment on column public.orders.total is 'Order total (e.g. dollars).';
comment on column public.orders.latitude is 'Delivery latitude (WGS84).';
comment on column public.orders.longitude is 'Delivery longitude (WGS84).';
comment on column public.orders.accuracy is 'Optional position accuracy in meters.';

alter table public.orders enable row level security;

create policy "Allow anon insert on orders"
  on public.orders for insert to anon with check (true);

-- Required for polling scripts (get_orders.py / fetchandfly.py) when using anon key
create policy "Allow anon read orders"
  on public.orders for select to anon using (true);
