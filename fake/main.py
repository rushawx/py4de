import json
import random
import os
import uuid
from dataclasses import fields

import psycopg2
from faker import Faker
from faker.providers import DynamicProvider
from schemas import (
    Database,
    LoyaltyStatusEnum,
    OrderDetailsTable,
    OrdersTable,
    OrderStatusEnum,
    ProductCategoryEnum,
    ProductCategoryTable,
    ProductsTable,
    UsersTable,
)
from sqlalchemy import create_engine

product_categories_provider = DynamicProvider(
    provider_name="product_categories",
    elements=[
        ProductCategoryEnum.SMARTPHONE,
        ProductCategoryEnum.TABLET,
        ProductCategoryEnum.LAPTOP,
        ProductCategoryEnum.DESKTOP,
    ],
)

loyalty_status_provider = DynamicProvider(
    provider_name="loyalty_status",
    elements=[
        LoyaltyStatusEnum.BRONZE.value,
        LoyaltyStatusEnum.SILVER.value,
        LoyaltyStatusEnum.GOLD.value,
        LoyaltyStatusEnum.PLATINUM.value,
    ],
)

order_status_provider = DynamicProvider(
    provider_name="order_status",
    elements=[
        OrderStatusEnum.PENDING.value,
        OrderStatusEnum.COMPLETED.value,
        OrderStatusEnum.CANCELLED.value,
    ],
)

fake = Faker("ru_RU")

fake.add_provider(product_categories_provider)
fake.add_provider(loyalty_status_provider)
fake.add_provider(order_status_provider)

PG_DSN = f"postgresql://{os.getenv('PG_DB_USER')}:{os.getenv('PG_DB_PASSWORD')}@{os.getenv('PG_DB_HOST')}:{os.getenv('PG_DB_PORT')}/{os.getenv('PG_DB_NAME')}"

pg_engine = create_engine(PG_DSN)
pg_connection = pg_engine.raw_connection()
pg_cursor = pg_connection.cursor()

users_data = []

for _ in range(100):

    users_data.append((
        uuid.uuid4(),
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number(),
        fake.date_time(),
        fake.loyalty_status(),
    ))

pg_cursor.executemany(
    "insert into public.users values(%s, %s, %s, %s, %s, %s, %s)",
    users_data,
)
pg_connection.commit()

products_data = []

for _ in range(100):

    products_data.append((
        uuid.uuid4(),
        fake.word(),
        fake.text(),
        random.choice([
            '7deec2b6-180f-4fc5-acd5-758ba2c8c3ca',
            '233d515a-dcbd-4bbb-9c04-339c6b718285',
            '1e69f0e1-e072-41e6-be84-3a76830826a6',
            '197444fa-418c-4bdd-af82-f56a2f2f7d4a'
        ]),
        random.randint(1, 100000) / 100,
        random.randint(1, 1000),
        fake.date_time(),
    ))

pg_cursor.executemany(
    "insert into public.products values(%s, %s, %s, %s, %s, %s, %s)",
    products_data,
)
pg_connection.commit()

orders_data = []

for _ in range(100):
    orders_data.append((
        uuid.uuid4(),
        random.choice(users_data)[0],
        fake.date_time(),
        random.randint(1, 100000) / 100,
        fake.order_status(),
        fake.date_time()
    ))

pg_cursor.executemany(
    "insert into public.orders values(%s, %s, %s, %s, %s, %s)",
    orders_data,
)
pg_connection.commit()

order_details_data = []

for order in orders_data:
    for _ in range(random.randint(1, 10)):
        order_details_data.append((
            uuid.uuid4(),
            order[0],
            random.choice(products_data)[0],
            random.randint(1, 1000),
            random.randint(100, 100000) / 100,
            random.randint(100, 100000) / 100,
        ))

pg_cursor.executemany(
    "insert into public.order_details values(%s, %s, %s, %s, %s, %s)",
    order_details_data,
)
pg_connection.commit()
