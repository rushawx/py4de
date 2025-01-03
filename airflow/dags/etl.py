import datetime

from airflow.decorators import task
from airflow.models.dag import DAG

from dataclasses import fields

import dataclasses
import datetime
import uuid
from enum import Enum
from typing import Type, TypeVar


T = TypeVar("T")


class LoyaltyStatusEnum(Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class ProductCategoryEnum(Enum):
    SMARTPHONE = "smartphone"
    TABLET = "tablet"
    LAPTOP = "laptop"
    DESKTOP = "desktop"


class OrderStatusEnum(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclasses.dataclass
class UsersTable:
    user_id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    registration_date: datetime.datetime
    loyalty_status: LoyaltyStatusEnum


@dataclasses.dataclass
class ProductCategoryTable:
    category_id: uuid.UUID
    name: ProductCategoryEnum
    parent_category_id: uuid.UUID


@dataclasses.dataclass
class ProductsTable:
    product_id: uuid.UUID
    name: str
    description: str
    category_id: uuid.UUID
    price: float
    stock_quantity: int
    creation_date: datetime.datetime


@dataclasses.dataclass
class OrdersTable:
    order_id: uuid.UUID
    user_id: uuid.UUID
    order_date: datetime.datetime
    total_amount: float
    status: OrderStatusEnum
    delivery_date: datetime.datetime


@dataclasses.dataclass
class OrderDetailsTable:
    order_detail_id: uuid.UUID
    order_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    price_per_unit: float
    total_price: float


class Database(Enum):
    PRODUCT_CATEGORIES = (ProductCategoryTable, "product_categories")
    USERS = (UsersTable, "users")
    PRODUCTS = (ProductsTable, "products")
    ORDERS = (OrdersTable, "orders")
    ORDER_DETAILS = (OrderDetailsTable, "order_details")

    def __init__(self, data_schema: Type[T], table_name: str):
        self.data_schema = data_schema
        self.table_name = table_name


with DAG(
    dag_id="etl",
    start_date=datetime.datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
):

    @task
    def replicate():
        import pandas as pd
        from airflow.hooks.base import BaseHook
        from sqlalchemy.engine import create_engine

        pgh = BaseHook.get_connection("postgres")

        pg_dsn = f"postgresql://{pgh.login}:{pgh.password}@{pgh.host}:{pgh.port}/{pgh.schema}"

        pg_engine = create_engine(pg_dsn)
        pg_connection = pg_engine.raw_connection()
        pg_cursor = pg_connection.cursor()

        msh = BaseHook.get_connection("mysql")

        ms_dsn = f"mysql://{msh.login}:{msh.password}@{msh.host}:{msh.port}/{msh.schema}"

        ms_engine = create_engine(ms_dsn)
        ms_connection = ms_engine.raw_connection()
        ms_cursor = ms_connection.cursor()

        for table in Database:

            pg_cursor.execute(f"select * from {table.table_name}")
            data = pg_cursor.fetchall()

            print(data)

            print(f"Table {table} has {len(data)} rows")

            ms_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            ms_connection.commit()
            ms_cursor.execute(f"TRUNCATE table {table.table_name}")
            ms_connection.commit()
            ms_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            ms_connection.commit()

            df = pd.DataFrame(data=data, columns=[f.name for f in fields(table.data_schema)])
            df.to_sql(f"{table.table_name}", ms_engine, if_exists="append", index=False)

    replicate_task = replicate()
