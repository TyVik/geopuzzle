from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper


def query(statement, **kwargs):
    sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
    sparql.setQuery(statement.format(**kwargs))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {'wiki': 'https://{language}.wikipedia.org/wiki/{name}'.format(**kwargs), 'name': kwargs['name']}
    if len(results) > 0:
        results = results[0]
        for field in results:
            result[field] = results[field]['value']
    return result
