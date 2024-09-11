from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

items = [
    {
        "name": "Green Apple",
        "price": 19
    },
    {
        "name": "Momos",
        "price": 60
    },
    {
        "name": "Chicken Sandwich",
        "price": 120
    }
]

# get-items URL
# http://127.0.0.1:5000/get-items
@app.route('/get-items', methods=['GET'])
def get_items():
    return {"items": items}

# get-item individual URL
# http://127.0.0.1:5000/get-item
@app.route('/get-item', methods=['GET'])
def get_item():
    name = request.args.get('name')
    print(name)
    for item in items:
        if name == item['name']:
            return item
        
    return {"message": "Item does not exist"},404   

# add-item URL
# http://127.0.0.1:5000/add-item
@app.route('/add-item', methods=['POST'])
def add_item():
    request_data = request.get_json()
    items.append(request_data)
    return {"message": "Item added successfully"}, 201


# update URL
# http://127.0.0.1:5000/update-item
@app.route('/update-item', methods=['PUT'])
def update_item():
    request_data = request.get_json()
    for item in items:
        if item['name']== request_data['name']:
            item['price']=request_data['price']
            return {"message": "Item updated successfully"}
        
    return {"message": "IGiven Record Does Not Exixts"},404


# delete-item individual URL
# http://127.0.0.1:5000/delete-item
@app.route('/delete-item', methods=['DELETE'])
def delete_item():
    name = request.args.get('name')
    print(name)
    for item in items:
        if name == item['name']:
            items.remove(item)
            return {"message": "Item delete successfully"}
        
    return {"message": "Item does not exist"},404   

if __name__ == "__main__":
    app.run()
