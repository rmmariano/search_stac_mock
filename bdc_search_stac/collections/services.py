import os
import re
import json

import requests
from requests.auth import HTTPBasicAuth

class CollectionsServices():

    @classmethod
    def search_items(cls, url, collection_id, query):
        base_url = '{}/collections/{}/items?{}'.format(url, collection_id, query)
        r = requests.get(base_url, headers={})
        if r and r.status_code in (200, 201):
            return json.loads(r.text)
        return None

    @classmethod
    def search_collections(cls, url):
        base_url = '{}/collections?limit=1000'.format(url)
        r = requests.get(base_url, headers={})
        if r and r.status_code in (200, 201):
            return json.loads(r.text)
        return None