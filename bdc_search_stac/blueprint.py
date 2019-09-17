from flask import Blueprint
from flask_restplus import Api

from bdc_search_stac.collections.controller import api as collections_ns
from bdc_search_stac.providers.controller import api as providers_ns
from bdc_search_stac.status.controller import api as status_ns

blueprint = Blueprint('stac_compose', __name__, url_prefix='/stac_compose')

api = Api(blueprint, doc=False)

api.add_namespace(collections_ns)
api.add_namespace(providers_ns)
api.add_namespace(status_ns)