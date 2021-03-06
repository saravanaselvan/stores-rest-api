import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from resources.auth import Login
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserList, UserRegister

app = Flask(__name__)
uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sdlakjfoiuwerfsdlk;jsdflk;sdjf;ld'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Login, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)
