from typing import Dict, List, Set

from bs4 import BeautifulSoup
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

    def get_wiki_link(instance: str, langs: List) -> Dict:
        html = urlopen(instance)
        soup = BeautifulSoup(html)
        result = {}
        for lang in langs:
            link = soup.find("a", attrs={'hreflang': lang})
            result[lang] = {'wiki': link.get('href'), 'name': link.get('title')}
        return result

    sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
    sparql.setQuery(statement.format(**kwargs))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {}
    for row in results:
        lang = row.pop('lang')['value']
        result[lang] = prepare_row(row)

    wiki_links = get_wiki_link(result['en']['instance'], list(result.keys()))
    for lang, values in wiki_links.items():
        result[lang]['wiki'] = values['wiki']
        result[lang]['name'] = values['name']
    return result
