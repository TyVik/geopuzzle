from django.core.files.storage import default_storage

from cairosvg.surface import PNGSurface
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
            if field == 'area':
                result[field] = str(int(float(results[field]['value'])))
                """
            if field == 'flag':
                png_name = 'flags/' + results[field]['value'].split('/')[-1].replace('svg', 'png')
                png_path = default_storage.path(png_name)
                PNGSurface.convert(url=results[field]['value'], write_to=png_path)
                result[field] = default_storage.url(png_name)
                """
            else:
                result[field] = results[field]['value']
    return result
