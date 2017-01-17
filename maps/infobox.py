from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper

STATEMENT = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>


SELECT ?country ?name ?capital ?area ?population ?thumbnail (group_concat(?language;separator=",") as ?languages) WHERE {{
    ?country a dbo:Country.
    ?country rdfs:label ?name.
    ?country dbo:capital ?capital_raw.
    ?capital_raw dbp:name ?capital.
    ?country dbp:areaKm ?area.
    ?country dbo:populationTotal ?population.
    ?country dbo:thumbnail ?thumbnail.

    OPTIONAL {{?country dbo:officialLanguage ?language}}

    FILTER (?name = "{}"@en)
}} group by ?country ?name ?capital ?area ?population ?thumbnail
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
            result[field] = results[field]['value']
    return result
