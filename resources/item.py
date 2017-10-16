from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help = "Every item needs a store id!"
    )
    #the price is the only one in the parse argument so all other fields would be discarded when parsing
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #400 means something wrong with the request, 500 is the server had problem

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message:" "An error occurred inserting the item"}, 500 #default is 200, important to return 500 because it is not the users fault

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() #Parser makes sure that only the price is being updated, not the name

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            #item.store_id = data['store_id']
        else:
            item = ItemModel(name, data['price'], data['store_id'])

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #[item.json() for item in ItemModel.query.all()]
