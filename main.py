import uuid
import json
from flask import Flask, request

app = Flask(__name__)

# Load initial data from data.json if exists
try:
    with open('data.json', 'r') as f:
        items = json.load(f)
except FileNotFoundError:
    # If data.json doesn't exist, initialize with items from db.py
    from db import items

# get-items URL
@app.route('/items', methods=['GET'])
def get_items():
    return {"items": items}

# get-item individual URL
@app.route('/item', methods=['GET'])
def get_item():
    id = request.args.get('id')
    try:
        return items[id]
    except KeyError:
        return {"message": "Item does not exist"}, 404

# add-item URL
@app.route('/item', methods=['POST'])
def add_item():
    request_data = request.get_json()
    if not request_data:
        return {"message": "Request body is empty"}, 400

    if 'name' not in request_data or 'price' not in request_data:
        return {"message": "'name' and 'price' must be included in body"}, 400

    # Check if the item already exists
    for item_id, item_value in items.items():
        if item_value['name'] == request_data['name']:
            return {"message": f"Item '{request_data['name']}' already exists with ID {item_id}"}, 400

    new_id = uuid.uuid4().hex
    items[new_id] = request_data

    # Save the data to the file
    save_items_to_file()

    return {"message": "Item added successfully"}, 201

# update-item URL
@app.route('/item', methods=['PUT'])
def update_item():
    id = request.args.get('id')
    if not id or id not in items:
        return {"message": "Given ID not found"}, 404

    request_data = request.get_json()
    if 'name' not in request_data or 'price' not in request_data:
        return {"message": "'name' and 'price' must be included in body"}, 400

    # Update the item
    items[id] = request_data

    # Save the data to the file
    save_items_to_file()

    return {"message": "Item updated successfully"}, 200

# delete-item URL
@app.route('/item', methods=['DELETE'])
def delete_item():
    id = request.args.get('id')
    if id in items:
        del items[id]
        
        # Save the data to the file
        save_items_to_file()

        return {"message": "Item deleted successfully"}
    
    return {"message": "Item does not exist"}, 404

# Utility function to save items to the file
def save_items_to_file():
    with open('data.json', 'w') as f:
        json.dump(items, f)

if __name__ == "__main__":
    app.run()

