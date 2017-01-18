from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper

STATEMENT = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT ?country ?name ?capital ?area ?population ?thumbnail ?wiki WHERE {{
    ?country a dbo:Country.
    ?country rdfs:label ?name.
    ?country dbo:capital ?capital.
    ?country dbp:areaKm ?area.
    ?country dbo:populationTotal ?population.
    ?country foaf:isPrimaryTopicOf ?wiki.
    ?country dbo:thumbnail ?thumbnail.

    FILTER (?name = "{}"@en)
}}
"""


def query(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(STATEMENT.format(name))
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
