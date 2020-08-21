# Misc functions you'll need in the API
from app.auth.models import User
from app.products.models import Product
from flask import jsonify
from werkzeug.security import check_password_hash

def user_exists(username):
    if User.objects(username=username).first():
        return True
    else:
        return False

def product_exists(product_name):
    if Product.objects(name=product_name).first():
        return True
    else:
        return False

# Output status generator
def generate_status(status, msg):
    return jsonify({'status': status, 'msg': msg})

def verify_pw(username, password):
    check_user = User.objects(username=username).first()
    if check_password_hash(check_user['password'], password):
        return True
    else:
        return False

# Credential checker
def verify_credentials(username, password):
    if not user_exists(username):
        return generate_status(301, "Invalid username"), True

    # password checker
    if not verify_pw(username, password):
        return generate_status(401, "Incorrect password"), True

    return None, False

# Change product quantity
def update_quantity(data, operation):

    # User authentication
    response, error = verify_credentials(data['username'], data['password'])
    if(error):
        return response

    if data['quantity'] < 0:
        return generate_status(304, 'Invalid quantity of items.')

    product = Product.objects(name=data['name']).first()

    if not product:
        return generate_status(312, 'Invalid product name.')

    if operation == "buy":
        new_quantity = product['quantity'] + data['quantity']
    else:
        new_quantity = product['quantity'] - data['quantity']
        if new_quantity < 0:
            return generate_status(313, 'Not enough items on stock.')

    Product.objects(name=product['name']).update(set__quantity=new_quantity)

    return generate_status(200, 'Success.')

def update_price(name, value, price_kind):
    if data[price_kind]:
        try:
            Product.objects(name=product[name]).update(set__buy_price=value)
        except:
            return generate_status(500, 'Internal server error.')
