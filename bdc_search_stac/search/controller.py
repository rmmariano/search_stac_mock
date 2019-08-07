import os, json
from flask import request
from werkzeug.exceptions import InternalServerError, BadRequest
from werkzeug.datastructures import ImmutableMultiDict

from bdc_search_stac.search import ns
from bdc_search_stac.search.business import SearchBusiness
from bdc_search_stac.search.parsers import validate
from bdc_core.utils.flask import APIResource

api = ns

@api.route('/')
class SearchController(APIResource):

    def get(self):
        data, status = validate(request.args.to_dict(flat=True), 'search')
        if status is False:
            raise BadRequest(json.dumps(data))

        """
        Search RF in STAC's
        """
        return SearchBusiness.search(**request.args)

@api.route('/providers')
class SearchProviderController(APIResource):

    def get(self):
        """
        List of STAC providers
        """
        providers = SearchBusiness.get_providers()

        return {
            "providers": providers
        }