from datetime import datetime
from uuid import UUID  # universally unique identifier

from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import CreateOrderSchema # We import the pydantic models so we can use them for validation

# Define an order object to return in our responses
order = {
    'id': 'ff0f1355-e821-4178-9567-550dec27a373',
    'status': 'delivered',
    'created': datetime.utcnow(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

# Register a GET endpoint for the /orders URL path
@app.get('/orders') # decorators @
def get_orders():
    return {'orders': [orders]}

# Specify that the response's status code is 201 (Created)
@app.post('/orders', status_code=status.HTTP_201_CREATED) 
def create_order(order_details: CreateOrderSchema):
    return order

# Define URL parameters, such as order_id, within curly brackets
@app.get('/orders/{order_id}')
def get_order(order_id: UUID):  # Capture the URL parameter as a function argument
    return order

@app.put('/orders/{order_id}')
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    return order

# Use HTTPStatus.NO_CONTENT.value to return an empty response
@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
    return order

@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
    return order

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
