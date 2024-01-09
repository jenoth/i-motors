# i-motors
Innovative high-quality car parts sellers, i-motors

### Modules / Apps
- Customers
- Products
- Cart / Shopping Cart / Basket
- Order
- OrderItems

### Usecases
- Customer can view all the products.
    - Can view the paginated products
    - Can view the filtered products
- Customer can view the product details
- Customer can order the products process
  - First step of the ordering process is adding the items in a cart/basket
  - Then, Submitting the basket. Placing the order.
  - Choose the delivery option(home delivery / drive-through / counter collection)
  - Payments method can be selected
  - Ready for delivery
  - Successfully handed over(delivered) to the customer
  - Customer/business can cancel the order at any time
  - Order will be kept in database to reorder/ check later

### Database(ER) Design
- Customer can have many carts. But, can have only one active cart
- One cart can have many products. One product can be put in many carts. (OrderItems table acts as joining table)
- One cart only can be used for one order. like wise, one order cannot be in many carts
- One customer can have many orders. One order belongs to only one customer

**customer - order** _one to many_
**customer - cart** _one to many_
**cart - order** _one to many_
**cart - product** _many to many_

### Implemented functionalities
- get all products
- view the details of a product
- basket can be created
- **In basket,** products can be added, added products can be changed, added products can be removed
- Basket can be submitted to place the order

### Improvements
- Customer and User should be mapped together
- Additional fields can be added for an entity
- Proper validation(api request validation and db level validation), error handling and logging
- Proper code documentation
- Type hints(I personally don't like it :D)
- Well structured APIs(url, request payload, unique response body)
- Can be applied DRY principal and code organization
- Some complex logic can be simplified but, It depends on the API consumers, specially front-end service

### System Used for development (OS, Ubuntu 20.04.6 LTS)

### Python version used (required Python 3.8+)
[Python 3.9.8](https://docs.python.org/3.9/)

### Local Setup
#### Run the Docker locally using Makefile
```
make build-and-run-docker-locally
```
###### Open the browser and see the output
- [OpenAPI Specification of our service](http://localhost:8000/ui/)
- [Read the DOCs of our service](http://localhost:8000/redoc/)

#### Virtual environment setup and installing the requirements
```
$ python3.9 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade setuptools pip
$ pip install -r requirements/dev-requirements.txt
```

#### Creating a Django project and creating required apps
```
$ django-admin startproject autocompany .
$ cd autocompany/
$ django-admin startapp customers
$ django-admin startapp products
$ django-admin startapp carts
$ django-admin startapp cartitems
$ django-admin startapp orders
```

#### Initial database migrations and creating a superuser
```
change the directory to it's root redirectory. In our case manage.py resides here.
$ cd ..
$ python manage.py migrate
$ python manage.py createsuperuser --email admin@i-motors.com --username admin
```

#### Further database migrations
```
$ python manage.py makemigrations
$ python manage.py migrate
```

## Resources
_*Documentation*_
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [drf-yasg - Yet another Swagger generator](https://drf-yasg.readthedocs.io/en/stable/index.html)
 
_*PyPI*_
- [Django](https://pypi.org/project/Django/4.2.6/)
- [Django REST framework](https://pypi.org/project/djangorestframework/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [drf-yasg](https://pypi.org/project/drf-yasg/)
- [OpenAPI](https://www.openapis.org/)

_*GitHub*_
- [i-motors](https://github.com/jenoth/i-motors) **-** _**latest code is available in main branch**_
