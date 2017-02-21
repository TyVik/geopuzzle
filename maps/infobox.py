from typing import Dict

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
        result[lang]['wiki'] = 'https://{language}.wikipedia.org/wiki/{name}'.format(language=lang, name=result[lang]['name'])
    return result
