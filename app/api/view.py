from flask import Blueprint, request
from app.auth.models import User
from app.products.models import Product
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.functions import *

api = Blueprint('api', __name__, url_prefix='/api')

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if user_exists(username):
            return generate_status(309, 'Username already taken.')

        hashpass = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashpass)
        user.save()

        return generate_status(200, 'User successfully created.')

class AddProduct(Resource):
    def post(self):
        data = request.get_json()

        # User authentication
        response, error = verify_credentials(data['username'], data['password'])
        if(error):
            return response

        # Check for empty fields
        if not data['name']:
            return generate_status(311, 'Product name required.')

        if product_exists(data['name']):
            return generate_status(310, 'Product already registered.')

        if data['quantity'] < 0:
            return generate_status(304, 'Invalid quantity of items.')

        try:
            product = Product(name=data['name'], \
            description=data['description'], \
            quantity=data['quantity'], \
            buy_price=data['buy_price'], \
            sell_price=data['sell_price'])
        except KeyError:
            return generate_status(400, "Please check all product fields.")
        product.save()

        return generate_status(200, 'Product successfully created.')

class Buy(Resource):
    def post(self):
        # Needs: user authentication data, quantity and product name
        data = request.get_json()
        return update_quantity(data, "buy")

class Sell(Resource):
    def post(self):
        # Needs: user authentication data, quantity and product name
        data = request.get_json()
        return update_quantity(data, "sell")

class UpdatePrice(Resource):
    def post(self):
        data = request.get_json()

        # User authentication
        response, error = verify_credentials(data['username'], data['password'])
        if(error):
            return response

        try:
            if data['buy_price']:
                Product.objects(name=data['name']).update(set__buy_price=data['buy_price'])
        except KeyError:
            pass

        try:
            if data['sell_price']:
                Product.objects(name=data['name']).update(set__sell_price=data['sell_price'])
        except KeyError:
            pass

        return generate_status(200, 'Success.')
