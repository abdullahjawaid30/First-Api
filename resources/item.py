from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
import uuid
import json
from db import items  # Assuming this is the correct import path

blp = Blueprint("items", __name__, description="Operations on items")

def save_items_to_file():
    with open('data.json', 'w') as f:
        json.dump(items, f)

class Item(MethodView):
    def get(self):
        id = request.args.get('id')  # Retrieve ID from query parameters
        if id is None:
            return jsonify({"items": items})
        if id in items:
            return jsonify(items[id])
        return jsonify({"message": "Item does not exist"}), 404


    def post(self):
        request_data = request.get_json()
        if not request_data or 'name' not in request_data or 'price' not in request_data:
            return jsonify({"message": "'name' and 'price' must be included in the body"}), 400

        # Check if the item already exists by name
        for item_id, item_value in items.items():
            if item_value['name'] == request_data['name']:
                return jsonify({"message": f"Item '{request_data['name']}' already exists with ID {item_id}"}), 400

        # Generate new ID and add item
        new_id = uuid.uuid4().hex
        items[new_id] = request_data
        save_items_to_file()
        return jsonify({"message": "Item added successfully", "item_id": new_id}), 201

    def put(self):
        id = request.args.get('id')  # Retrieve ID from query parameters
        if not id or id not in items:
            return jsonify({"message": "Item with given ID not found"}), 404

        request_data = request.get_json()
        if 'name' not in request_data or 'price' not in request_data:
            return jsonify({"message": "'name' and 'price' must be included in the body"}), 400

        # Update the item
        items[id] = request_data
        save_items_to_file()
        return jsonify({"message": "Item updated successfully"}), 200

    def delete(self):
        id = request.args.get('id')  # Retrieve ID from query parameters
        if id in items:
            del items[id]
            save_items_to_file()
            return jsonify({"message": "Item deleted successfully"})
        return jsonify({"message": "Item does not exist"}), 404

# Register the routes with the blueprint for generic item actions
blp.add_url_rule("/items", view_func=Item.as_view("items"), methods=["GET", "POST", "PUT", "DELETE"])
