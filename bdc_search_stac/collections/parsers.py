from cerberus import Validator
from datetime import datetime

from bdc_search_stac.providers.parsers import validate_providers, providers

def validate_date(s):
    dates = s.split("/")
    for date in dates:
        if date.split('T')[0] and not datetime.strptime(date.split('T')[0], '%Y-%m-%d'):
            return None
    return s

def validate_collections(collections):
    ps = [p.split(':')[0] for p in collections.split(',')]
    if not validate_providers(','.join(ps)):
        return None
    return collections

def validate_bbox(box):
    list_bbox = box.split(',')
    coordinates = [float(b) for b in list_bbox]
    return coordinates if len(coordinates) == 4 else None

def validate_cloud(cloud):
    return float(cloud) if float(cloud) > 0 and float(cloud) <= 100 else None

def validate_limit(limit):
    return int(limit) if float(limit) > 0 else None

def search():
    base = {
        'collections': {"type": "string", "coerce": validate_collections, "empty": False, "required": True},
        'bbox': {"type": "list", "coerce": validate_bbox, "empty": False, "required": True},
        'cloud': {"type": "number", "coerce": validate_cloud, "empty": True, "required": False},
        'time': {"type": "string", "coerce": validate_date, "empty": True, "required": False},
        'limit': {"type": "number", "coerce": validate_limit, "empty": True, "required": False}
    }
    return base

def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True