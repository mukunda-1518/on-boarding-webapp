# Web App - Week1

## Installations
* ```git clone https://github.com/mukunda-1518/on-boarding-webapp.git```
* ```git checkout master```
* ```set up virtualenv, use python2 to create virtual env,```
* ```pip install -r requirements.txt```
* ```python manage.py runserver```

## Built With
* Python
* Django
* TastyPie
* JWT Authentication
* Celery
* RabbitMQ

## API Endpoints

### Authentication
* ```POST /api/v1/user/signup/``` - Register new user
* ```POST /api/v1/user/login/``` - Login

### Stores
* ```POST /api/v1/create_store/``` - Create a new store
* ```GET /api/v1/get_stores/{id}``` - Get the store details
* ```GET /api/v1/get_stores/``` - List all the stores details
* ```PUT /api/v1/get_stores/{id}``` - Updates the store and creates if store doesn't exists
* ```DEL /api/v1/get_stores/{id}``` - Delete's the store

### Items
* ```POST /api/v1/get_stores/{store_id}/create_item/``` - Creates item in for the given store id
* ```GET /api/v1/get_stores/{store_id}/get_items/{item_id}/``` - Gives the details of an item with given id
* ```GET /api/v1/get_stores/{store_id}/get_items/``` -  List all the items present in the given store id
* ```PUT /api/v1/get_stores/{store_id}/update_item/{item_id}/``` - Updated the item if present else creates new item
* ```DEL /api/v1/get_stores/{store_id}/delete_item/{item_id}/``` - Delete's given item in the store

### Orders
* ```POST /api/v1/create_order/``` - Creates an order
* ```GET /api/v1/get_orders/{order_id}/``` - Gives the details of given order (items, store details of an order)
* ```GET /api/v1/get_orders/``` - List all the orders of the user
* ```GET /api/v1/all_orders/``` - List all the orders of all the stores that are owned by the merchant (user). Only accessed by user with merchant role
* ```POST /api/v1/order/``` - Creates an order
* ```GET /api/v1/order/{order_id}``` - Gives the details of given order
* ```GET /api/v1/order/``` - List all the orders of the user

#### Postman Collection (API Docs) - https://www.postman.com/mukundapm/workspace/public-workspace/collection/24604602-03ffd114-9b78-4915-9772-0b7603e1abf7?ctx=documentation
