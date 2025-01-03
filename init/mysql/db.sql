create table if not exists db.product_categories (
    category_id char(36) primary key default (UUID()),
    name varchar(255),
    parent_category_id char(36) default null
);

insert into db.product_categories (category_id, name)
values ('7deec2b6-180f-4fc5-acd5-758ba2c8c3ca', 'smartphone'),
       ('233d515a-dcbd-4bbb-9c04-339c6b718285', 'tablet'),
       ('1e69f0e1-e072-41e6-be84-3a76830826a6', 'laptop'),
       ('197444fa-418c-4bdd-af82-f56a2f2f7d4a', 'desktop')
;

create table if not exists db.users (
    user_id char(36) primary key default (UUID()),
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null unique,
    phone varchar(255) not null unique,
    registration_date timestamp default current_timestamp,
    loyalty_status varchar(255) default 'Bronze'
);

create table if not exists db.products (
    product_id char(36) primary key default (UUID()),
    name varchar(255) not null,
    description text default null,
    category_id char(36),
    price float not null check (price > 0),
    stock_quantity integer not null check (stock_quantity >= 0),
    creation_date timestamp default current_timestamp,
    foreign key (category_id) references db.product_categories (category_id)
);

create table if not exists db.orders (
    order_id char(36) primary key default (UUID()),
    user_id char(36),
    order_date timestamp default current_timestamp,
    total_amount float not null check (total_amount > 0),
    status varchar(255) not null,
    delivery_date timestamp default current_timestamp,
    foreign key (user_id) references db.users (user_id)
);

create table if not exists db.order_details (
    order_detail_id char(36) primary key default (UUID()),
    order_id char(36),
    product_id char(36),
    quantity integer not null check (quantity > 0),
    price_per_unit float not null check (price_per_unit > 0),
    total_price float not null check (total_price > 0),
    foreign key (order_id) references db.orders (order_id),
    foreign key (product_id) references db.products (product_id)
);

create view db.data_mart as
select
	u.user_id,
	u.loyalty_status,
	coalesce(avg(od.quantity), 0) as quantity_avg,
	coalesce(avg(od.price_per_unit), 0) as price_per_unit_avg,
	coalesce(avg(od.total_price), 0) as total_price_avg
from db.users u
	left join db.orders o using(user_id)
	left join db.order_details od using(order_id)
group by
	u.user_id,
	u.loyalty_status;