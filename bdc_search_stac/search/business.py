import json
import os
from pprint import pprint

from bdc_search_stac.search.services import SearchServices
from bdc_search_stac.config import BASE_DIR

class SearchBusiness():

    @classmethod
    def get_providers(cls):
        with open('{}/search/static/providers.json'.format(BASE_DIR)) as p:
            data = json.load(p)
        
        providers = {}
        for key in data.keys():
            providers[key] = data[key]['url']
        return providers
        
    @classmethod
    def search(cls):
        return {}