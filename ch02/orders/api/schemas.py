from enum import Enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, conlist, conint

class Size(Enum):   # We declare an enumeration schema
    small = 'small'
    medium = 'medium'
    big = 'big'

class Status(Enum):
    created = 'created'
    progress = 'progress'
    cancelled = 'cancelled'
    dispatched = 'dispatched'
    delivered = 'delivered'

class OrderItemSchema(BaseModel):   # Every pydantic model inherits from pydantic's BaseModel
    product: str    # We use Python-type hints to specify the type of attribute
    size: Size      # We constrain the values of a property by setting its type to enumeration
    quantity: Optional[conint(ge=1, strict=True)] = 1   # We specify quantity's minimum value and we give it a default

class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_length=1)    # We use pydantic's conlist type to define a list with at least one element

class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: Status

class GetOrderSchema(BaseModel):
    orders: List[GetOrderSchema]

