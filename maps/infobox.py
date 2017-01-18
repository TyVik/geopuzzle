from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper


def query(statement, name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(statement.format(name))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {}
    if len(results) > 0:
        results = results[0]
        for field in results:
            value = results[field]['value']
            if field == 'capital':
                value = value.split('/')[-1]
            result[field] = value
    return result
