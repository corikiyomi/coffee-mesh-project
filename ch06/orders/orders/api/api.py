import time
import uuid

from datetime import datetime
from uuid import UUID
from typing import Optional

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema
)

ORDERS =[]  # We represent our in-memory list of orders as a Python list

# Define an order object to return in our responses
order = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created': datetime.utcnow(),
    'updated': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None): # We include URL query parameters in the function signature
    if cancelled is None and limit is None: # If the parameters haven't been set, we return immediately
        return {'orders': ORDERS}
    
    query_set = [order for order in ORDERS] # If any of the parameters has been set, we filter list into a query_set

    if cancelled is not None:   # We check whether cancelled is set
        if cancelled:
            query_set = [
                order for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order for order in query_set
                if order['status'] != 'cancelled'
            ]
    if limit is not None and len(query_set) > limit: #  If limit is set and its value is lower than the length of query_set, we return a subset of query_set
        return {'orders': query_set[:limit]}
    
    return {'orders': query_set}

@app.post(
    '/orders', 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
) 
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    ORDERS.append(order)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order
        raise HTTPException(
            status_code=404, detail=f'Order with ID {order_id} not found'
        )

@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return order

@app.delete(
    '/orders/{order_id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(index)
            return Response(status_code=HTTPStatus.NO_CONTENT.value)
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException (
        status_code=404, detail=f'Order with ID {order_id} not found'
    )

{
    'detail': [
        {
            'loc': [
                'body',
                'order',
                0,
                'product'
            ],
            'msg': 'field required',
            'type': 'value_error.missing'
        }
    ]
}
