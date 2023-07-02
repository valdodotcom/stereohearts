from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, index_name, **kwargs):
    index = get_index(index_name)
    params = {}
    tags = ""
    if tags in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params['tagFilters'] = tags
    results = index.search(query)
    return results

def get_multiple_queries(query_string):
    queries = [
        { 'indexName': 'search_MusicList', 'query': query_string },
        { 'indexName': 'search_Review', 'query': query_string },
        { 'indexName': 'search_User', 'query': query_string },
        { 'indexName': 'search_Project', 'query': query_string },
        { 'indexName': 'search_Artist', 'query': query_string },
    ]
    client = get_client()
    results = client.multiple_queries(queries)
    return results