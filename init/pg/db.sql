create extension if not exists "uuid-ossp";

create table if not exists public.product_categories (
    category_id uuid primary key default uuid_generate_v4(),
    name varchar(255),
    parent_category_id uuid default null
);

insert into public.product_categories (category_id, name)
values ('7deec2b6-180f-4fc5-acd5-758ba2c8c3ca', 'smartphohe'),
       ('233d515a-dcbd-4bbb-9c04-339c6b718285', 'tablet'),
       ('1e69f0e1-e072-41e6-be84-3a76830826a6', 'laptop'),
       ('197444fa-418c-4bdd-af82-f56a2f2f7d4a', 'desktop')
;

create table if not exists public.users (
    user_id uuid primary key default uuid_generate_v4(),
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null unique,
    phone varchar(255) not null unique,
    registration_date timestamp with time zone default current_timestamp,
    loyalty_status varchar(255) default 'Bronze'
);

create table if not exists public.products (
    product_id uuid primary key default uuid_generate_v4(),
    name varchar(255) not null,
    description text default null,
    category_id uuid references public.product_categories (category_id),
    price float not null check (price > 0),
    stock_quantity integer not null check (stock_quantity >= 0),
    creation_date timestamp with time zone default current_timestamp
);

create table if not exists public.orders (
    order_id uuid primary key default uuid_generate_v4(),
    user_id uuid references public.users (user_id),
    order_date timestamp with time zone default current_timestamp,
    total_amount float not null check (total_amount > 0),
    status varchar(255) not null,
    delivery_date timestamp with time zone default current_timestamp
);

create table if not exists public.order_details (
    order_detail_id uuid primary key default uuid_generate_v4(),
    order_id uuid references public.orders (order_id),
    product_id uuid references public.products (product_id),
    quantity integer not null check (quantity > 0),
    price_per_unit float not null check (price_per_unit > 0),
    total_price float not null check (total_price > 0)
);

create table if not exists public.health_check (
    status TEXT,
    created timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

insert into public.health_check (status)
values ('ready')
;
