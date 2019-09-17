import os, json
from flask import request
from werkzeug.exceptions import InternalServerError, BadRequest
from werkzeug.datastructures import ImmutableMultiDict

from bdc_search_stac.collections import ns
from bdc_search_stac.collections.business import CollectionsBusiness
from bdc_search_stac.collections.parsers import validate
from bdc_core.utils.flask import APIResource

api = ns

@api.route('/')
class ItemsController(APIResource):

    def get(self):
        data, status = validate(request.args.to_dict(flat=True), 'providers')
        if status is False:
            raise BadRequest(json.dumps(data))

        """
        List of STAC collections by providers
        """
        return CollectionsBusiness.get_collections_by_providers(data['providers'])

@api.route('/items')
class CollectionsController(APIResource):

    def get(self):
        data, status = validate(request.args.to_dict(flat=True), 'search')
        if status is False:
            raise BadRequest(json.dumps(data))

        """
        Search RF in STAC's
        """
        features = CollectionsBusiness.search(**request.args)

        return {
            "meta": {
                "found": len(features)
            },
            "features": features
        }
