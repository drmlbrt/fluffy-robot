from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, timedelta

from resources.user import UserRegister
from security import authenticate, identity
from resources.item import ItemList, Item
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key_that_is_long_and_complicated'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_ATH_URL_RULE'] = "/login"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

jwt = JWT(app, authenticate, identity)  # /auth  it creates a new endpoint, without creating it yourself!
'''It shall return a jwt token when the user is authenticated. It will 
be used for a new request, using the token. So if valid authentication, then requests can be made'''

db.init_app(app)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        "access_token": access_token.decode('utf-8'),
        "user_id": identity.id,
        "user_name": identity.username
    })


# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify({
#         "message": error.description,
#         "code": error.status_code
#     }), error.status_code


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/itemname
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
app.run(port=5000, debug=True)
