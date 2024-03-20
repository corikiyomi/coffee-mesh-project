import time
import uuid

from datetime import datetime
from uuid import UUID  # universally unique identifier

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    CreateOrderSchema, # We import the pydantic models so we can use them for validation
    GetOrderSchema,
    GetOrdersSchema
)

ORDERS =[]  # We represent our in-memory list of orders as a Python list


# Define an order object to return in our responses
# order = {
#     'id': 'ff0f1355-e821-4178-9567-550dec27a373',
#     'status': 'delivered',
#     'created': datetime.utcnow(),
#     'updated': datetime.utcnow(),
#     'order': [
#         {
#             'product': 'cappuccino',
#             'size': 'medium',
#             'quantity': 1
#         }
#     ]
# }

# Register a GET endpoint for the /orders URL path
@app.get('/orders', response_model=GetOrdersSchema) # decorators @
def get_orders():
    return ORDERS #  To return the list of orders, we simply return the ORDERS list

# Specify that the response's status code is 201 (Created)
@app.post(
    '/orders', 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
) 
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()    # We transform every order into a dictionary
    order['id'] = uuid.uuid4 #      We enrich the order object with server-side attributes, such as the id
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    ORDERS.append(order)    #   To create the order, we add it to the list
    return order #    After appending the order to the list, we return it

# Define URL parameters, such as order_id, within curly brackets
@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):  # Capture the URL parameter as a function argument
    for order in ORDERS: #      To find an order by ID, we iterate the ORDERS list and check their IDs
        if order['id'] == order_id:
            return order
        raise HTTPException( #  If an order isn't found, we raise an HTTPException with status_code set to 404 to return a 404 response
            status_code=404, detail=f'Order with ID {order_id} not found'
        )

@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return order

# Use HTTPStatus.NO_CONTENT.value to return an empty response
@app.delete(
    '/orders/{order_id}', 
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order(order_id: UUID):
    for index, order in enumerate(ORDERS): #    We order from the list using the list.pop() method
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
