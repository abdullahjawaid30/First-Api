from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import uuid
import json
from db import items  # items should follow the structure provided
from schemas import ItemSchema, ItemGetSchema, SuccessMessageSchema, ItemQuerySchema, ItemOptionalQuerySchema

blp = Blueprint("items", __name__, description="Operations on items")

def save_items_to_file():
    with open('data.json', 'w') as f:
        json.dump(items, f)

class Item(MethodView):
    @blp.response(200, ItemGetSchema(many=True))  # Correct response for returning many items
    @blp.arguments(ItemOptionalQuerySchema, location="query")
    def get(self, args):
        id = args.get('id')  # Retrieve ID from query parameters

        if id is None:  # If no ID is provided, return all items
            return items  # @blp.response will handle serialization

        # Find the item with the matching ID
        for item in items:
            if item['id'] == id:
                return [item]  # Return as a list to satisfy many=True

        # If no item is found with the given ID, return a 404 error
        abort(404, description="Record does not exist")

    @blp.arguments(ItemSchema)
    @blp.response(201, SuccessMessageSchema)  # Pass schema class, not instance
    def post(self, request_data):
        if not request_data or 'name' not in request_data or 'price' not in request_data:
            abort(400, description="'name' and 'price' must be included in the body")

        # Check if the item already exists by name
        for item in items:
            if item['item']['name'] == request_data['name']:
                abort(400, description=f"Item '{request_data['name']}' already exists")

        # Generate new ID and add item
        new_id = uuid.uuid4().hex
        new_item = {
            "id": new_id,
            "item": request_data
        }
        items.append(new_item)
        save_items_to_file()
        return {"message": "Item added successfully", "item_id": new_id}

    @blp.arguments(ItemSchema)
    @blp.response(200, SuccessMessageSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self, request_data, args):
        id = args.get('id')  # Retrieve ID from query parameters

        # Look for the item with the given ID
        for item in items:
            if item['id'] == id:
                # Update the nested 'item' dictionary
                item['item'].update(request_data)  
                save_items_to_file()  # Save the updated items to file
                return jsonify({"message": "Item updated successfully"}), 200

        # If no item with the given ID is found, return 404
        abort(404, description="Item with the given ID not found")

    @blp.response(200, SuccessMessageSchema)  # Pass schema class, not instance
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        id = args.get('id')  # Retrieve ID from query parameters
        if not id:
            abort(400, description="ID must be provided")  # Bad Request if no ID

        for i, item in enumerate(items):
            if item['id'] == id:
                del items[i]  # Delete the item from the list
                save_items_to_file()  # Save changes to file
                return {"message": "Item deleted successfully"}

        # If the item with the provided ID is not found, return 404
        abort(404, description="Item with the given ID does not exist")

# Register the routes with the blueprint for generic item actions
blp.add_url_rule("/items", view_func=Item.as_view("items"), methods=["GET", "POST", "PUT", "DELETE"])
