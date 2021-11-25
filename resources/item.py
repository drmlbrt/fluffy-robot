from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # initialize new object, run the request through the parser and match with arguments defined
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help="Every Item needs a store ID"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exists".format(name)}, 400  # 400 = Bad Request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "error occurred inserting the item in db"}, 500  # Internal server error

        return item.json(), 201

    def delete(self, name):

        if ItemModel.find_by_name(name) is None:
            return {'message': "An item with the name '{}' does NOT exist".format(name)}, 400  # 400 = Bad Request

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item {} deleted".format(name)}, 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # {'items': list(map(lambda x:x.json(), ItemModel.query.all()))}