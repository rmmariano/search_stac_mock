import json
import os
from pprint import pprint

from bdc_search_stac.config import BASE_DIR

class ProvidersBusiness():

    @classmethod
    def get_providers(cls):
        with open('{}/providers/static/providers.json'.format(BASE_DIR)) as p:
            data = json.load(p)

        providers = {}
        for key in data.keys():
            providers[key] = data[key]['url']
        return providers