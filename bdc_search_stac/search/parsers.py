from cerberus import Validator

from datetime import datetime

def search():
    return {
        'workspace': {"type": "string", "empty": False, "required": True},
        'datastore': {"type": "string", "empty": False, "required": True},
        'layer': {"type": "string", "empty": False, "required": True},
        'path': {"type": "string", "empty": False, "required": True},
        'description': {"type": "string", "empty": True, "required": False},
        'projection': {"type": "string", "empty": False, "required": True}
    }


def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))
    
    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True