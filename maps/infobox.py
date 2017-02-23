import json
from typing import Dict

from urllib.request import urlopen
# from cairosvg.surface import PNGSurface
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper


def query(statement: str, **kwargs) -> Dict:
    def prepare_row(row: Dict) -> Dict:
        for field in row:
            if field == 'area':
                row[field] = str(int(float(row[field]['value'])))
                """
            if field == 'flag':
                png_name = 'flags/' + results[field]['value'].split('/')[-1].replace('svg', 'png')
                png_path = default_storage.path(png_name)
                PNGSurface.convert(url=results[field]['value'], write_to=png_path)
                result[field] = default_storage.url(png_name)
                """
            else:
                row[field] = row[field]['value']
        return row

    sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
    sparql.setQuery(statement.format(**kwargs))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {}
    for row in results:
        lang = row.pop('lang')['value']
        result[lang] = prepare_row(row)

    if 'en' in result and 'instance' in result['en']:
        instance = result['en']['instance']
        response = urlopen(instance).read().decode('utf8')
        response = json.loads(response)
        for lang in result:
            try:
                links = response['entities'][instance.split('/')[-1]]['sitelinks']['{}wiki'.format(lang)]
                result[lang]['wiki'] = links['url']
                result[lang]['name'] = links['title']
            except:
                pass
    return result
