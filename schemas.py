from marshmallow import Schema,fields

class ItemSchema(Schema):
    name=fields.Str(required=True)
    price=fields.Int(required=True)
    
    

class ItemGetSchema(Schema):
     id=fields.Str(dump_only=True)
     item=fields.Nested(ItemSchema)
     
     
class SuccessMessageSchema(Schema):
    message=fields.Str(dump_only=True)
    

class ItemQuerySchema(Schema):
    id=fields.Str(required=True)
    
from marshmallow import Schema, fields

class ItemOptionalQuerySchema(Schema):
    id = fields.String(required=False)  # Mark the 'id' field as optional
