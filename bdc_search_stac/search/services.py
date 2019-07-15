import os
import re

import requests
from requests.auth import HTTPBasicAuth

class SearchServices():
    
    @classmethod
    def get_base_url(cls, content_type='application/json'):
        headers = {
            "content-type": content_type
        }
        base_url = os.environ.get('GEOSERVER_URL', 'http://localhost:8081/geoserver')
        auth = HTTPBasicAuth(
            os.environ.get('GEOSERVER_USER', 'admin'),
            os.environ.get('GEOSERVER_PASSWORD', 'geoserver')
        )
        return '{}'.format(base_url), headers, auth


    @classmethod
    def get_providers(cls, workspace):
        base_url, headers, auth = cls.get_base_url()
        base_url += '/rest/workspaces/{}/coveragestores.json'.format(workspace)
        r = requests.get(base_url, headers=headers, verify=False, auth=auth)
        if r and r.status_code in (200, 201):
            return r
        return None
