from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import jsonify

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id', type=int, required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200

        return {"message": "Item not available."}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f"Item already exists - {name}"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        item.save_to_db()
        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item = ItemModel(name, **data)

            item.save_to_db()
            return {"message": "Item updated."}

        return {"message": "Item not found."}, 400

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        item.delete_from_db()
        return {'message': 'Item deleted'}


class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
