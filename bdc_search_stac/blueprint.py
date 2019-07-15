from flask import Blueprint
from flask_restplus import Api

from bdc_search_stac.search.controller import api as search_ns
from bdc_search_stac.status.controller import api as status_ns

blueprint = Blueprint('stac', __name__, url_prefix='/stac')

api = Api(blueprint, doc=False)

api.add_namespace(search_ns)
api.add_namespace(status_ns)