from flask_restful import Api
from app import app
from app.api.view import Register, AddProduct, Buy, Sell, UpdatePrice

api = Api(app)

api.add_resource(Register, '/api/register')
api.add_resource(AddProduct, '/api/product/add')
api.add_resource(Buy, '/api/product/buy')
api.add_resource(Sell, '/api/product/sell')
api.add_resource(UpdatePrice, '/api/product/update-price')
