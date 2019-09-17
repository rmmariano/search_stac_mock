import os, json
from flask import request

from bdc_search_stac.providers import ns
from bdc_search_stac.providers.business import ProvidersBusiness
from bdc_search_stac.providers.parsers import validate
from bdc_core.utils.flask import APIResource

api = ns

@api.route('/')
class ProviderController(APIResource):

    def get(self):
        """
        List of STAC providers
        """
        providers = ProvidersBusiness.get_providers()

        return {
            "providers": providers
        }