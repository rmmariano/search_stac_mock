import json
import os
from pprint import pprint

from bdc_search_stac.collections.services import CollectionsServices
from bdc_search_stac.providers.business import ProvidersBusiness

class CollectionsBusiness():

    @classmethod
    def get_collections_by_providers(cls, providers):
        result_by_provider = {}
        for p in providers.split(','):
            response = CollectionsServices.search_collections(ProvidersBusiness.get_providers()[p])
            if response.get('collections'):
                result_by_provider[p] = [c['id'] for c in response['collections']]
            else:
                result_by_provider[p] = [c['title'] for c in response['links'] if c['rel'] == 'child']

        return result_by_provider

    @classmethod
    def search(cls, collections, bbox, cloud=False, time=False, limit=100):
        query = ''
        if time:
            # range temporal
            query += '&time={}'.format(time[0])
        if cloud:
            # cloud cover
            query += '&eo:cloud_cover=0/{}'.format(cloud[0])
        if limit:
            # limit
            # query += '&limit={}'.format(limit if int(limit) <= 1000 else 1000)
            query += '&limit={}'.format(limit if int(limit[0]) <= 1000 else 1000)

        result_features = []
        for cp in collections[0].split(','):
            cp = cp.split(':')
            provider = cp[0].upper()
            collection_id = cp[1]

            full_query = 'bbox={}{}'.format(('[{}]'.format(bbox[0]) if provider == 'DEVELOPMENT_SEED_STAC' else bbox[0]), query)
            response = CollectionsServices.search_items(ProvidersBusiness.get_providers()[provider], collection_id, full_query)

            # get all features
            if int(limit[0]) <= 1000 or not response.get('meta') or int(response['meta']['found']) <= 1000:
                if response:
                    result_features += response['features']

            # get 1000 features at a time
            else:
                response = CollectionsServices.search_items(ProvidersBusiness.get_providers()[provider], collection_id, full_query)
                if response:
                    qnt_all_features = response['meta']['found']
                    for x in range(0, int(qnt_all_features/1000)+1):
                        page_query = '{}&page={}'.format(full_query, (x+1))
                        response_by_page = CollectionsServices.search_items(ProvidersBusiness.get_providers()[provider], collection_id, page_query)
                        if response_by_page:
                            result_features += response_by_page['features']

        return result_features