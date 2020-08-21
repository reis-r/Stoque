from app import db

class Product(db.Document):
    meta = {'collection': 'products'}
    name = db.StringField(max_length=140, required=True)
    description = db.StringField(max_length=500)
    quantity = db.IntField()
    buy_price = db.FloatField()
    sell_price = db.FloatField()
