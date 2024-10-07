from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

items = [
    {"name": "Green Apple", "price": 19},
    {"name": "Momos", "price": 60},
    {"name": "Chicken Sandwich", "price": 120},
]

# get-items URL
@app.route('/items', methods=['GET'])
def get_items():
    return {"items": items}

# get-item individual URL
@app.route('/item', methods=['GET'])
def get_item():
    name = request.args.get('name')
    for item in items:
        if name == item['name']:
            return item
    return {"message": "Item does not exist"}, 404

# add-item URL
@app.route('/item', methods=['POST'])
def add_item():
    request_data = request.get_json()
    for item in items:
        if item['name'] == request_data['name']:
            return {"message": "Item already exists"}, 400

    items.append(request_data)
    return {"message": "Item added successfully"}, 201

# update-item URL
@app.route('/item', methods=['PUT'])
def update_item():
    request_data = request.get_json()
    for item in items:
        if item['name'] == request_data['name']:
            item['price'] = request_data['price']
            return {"message": "Item updated successfully"}
    return {"message": "Given record does not exist"}, 404

# delete-item URL
@app.route('/item', methods=['DELETE'])
def delete_item():
    name = request.args.get('name')
    for item in items:
        if name == item['name']:
            items.remove(item)
            return {"message": "Item deleted successfully"}
    return {"message": "Item does not exist"}, 404

if __name__ == "__main__":
    app.run()
