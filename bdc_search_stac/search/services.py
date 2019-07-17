import os
import re

import requests
from requests.auth import HTTPBasicAuth

class SearchServices():
    
    @classmethod
    def search_stac(cls, url, query):
        base_url = '{}?{}'.format(url, query)
        r = requests.get(base_url, headers={})
        if r and r.status_code in (200, 201):
            return r
        return None
