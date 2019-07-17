from cerberus import Validator
from datetime import datetime

from bdc_search_stac.search.business import SearchBusiness

def valide_date(s):
    return datetime.strptime(s, '%Y-%m-%d') if s else None

def valide_providers(providers):
    bdc_providers = SearchBusiness.get_providers().keys()
    for p in providers.split(','):
        if p not in bdc_providers:
            return None
    return providers.split(',')

def valide_bbox(box):
    list_bbox = box.split(',')
    coordinates = [float(b) for b in list_bbox]
    return coordinates if len(coordinates) == 4 else None

def valide_cloud(cloud):
    return float(cloud) if float(cloud) > 0 and float(cloud) <= 100 else None

def valide_limit(limit):
    return int(limit) if float(limit) > 0 else None


def search():
    return {
        'providers': {"type": "list", "coerce": valide_providers, "empty": False, "required": True},
        'bbox': {"type": "list", "coerce": valide_bbox, "empty": False, "required": True},
        'cloud': {"type": "number", "coerce": valide_cloud, "empty": False, "required": True},
        'start_date': {"type": "date", "coerce": valide_date, "empty": False, "required": True},
        'last_date': {"type": "date", "coerce": valide_date, "empty": False, "required": True},
        'limit_sat': {"type": "number", "coerce": valide_limit, "empty": True, "required": False}
    }

def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))
    
    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True