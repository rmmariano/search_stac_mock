import os, json
from flask import request
from werkzeug.exceptions import InternalServerError, BadRequest

from bdc_search_stac.search import ns
from bdc_search_stac.search.business import SearchBusiness
from bdc_search_stac.search.parsers import validate
from bdc_core.utils.flask import APIResource

api = ns

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