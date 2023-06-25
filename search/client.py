from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name='search_MusicList'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, **kwargs):
    index = get_index()
    params = {}
    tags = ""
    if tags in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params['tagFilters'] = tags
    results = index.search(query)
    return results