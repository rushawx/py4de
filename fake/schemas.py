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
