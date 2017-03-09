import json
from typing import Dict

from urllib.request import urlopen
# from cairosvg.surface import PNGSurface
import requests
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper


STATEMENT = """
SELECT DISTINCT ?lang {select} ?name ?flag ?coat_of_arms ?population ?area ?capital_name ?capital_id ?geonamesID ?capital_lon ?capital_lat WHERE {{
    {condition}
    {item_id} wdt:P17 wd:{country_id}.
    {item_id} rdfs:label ?name.
    BIND(LANG(?name) AS ?lang)
    FILTER((?lang = "ru") || (?lang = "en"))
    {item_id} wdt:P1566 ?geonamesID.
    OPTIONAL {{
        {item_id} wdt:P36 ?capital_id.
        ?capital_id p:P625 ?coordinates.
        ?coordinates psv:P625 ?coordinate_node.
        ?coordinate_node wikibase:geoLatitude ?capital_lat.
        ?coordinate_node wikibase:geoLongitude ?capital_lon.
        {item_id} wdt:P36/rdfs:label ?capital_name.
        FILTER(lang(?capital_name) = ?lang)
    }}
    OPTIONAL {{ {item_id} wdt:P41 ?flag. }}
    OPTIONAL {{ {item_id} wdt:P1082 ?population. }}
    OPTIONAL {{ {item_id} wdt:P2046 ?area. }}
    OPTIONAL {{ {item_id} wdt:P94 ?coat_of_arms. }}
}}
"""


def get_links(instance: str) -> Dict:
    result = {'en': {}, 'ru': {}}
    url = 'http://www.wikidata.org/entity/{}'.format(instance)
    response = urlopen(url).read().decode('utf8')
    response = json.loads(response)
    for lang in result:
        try:
            links = response['entities'][instance]['sitelinks']['{}wiki'.format(lang)]
            result[lang]['wiki'] = links['url']
            result[lang]['name'] = links['title']
            result[lang]['instance'] = url
        except:
            pass
    return result


def query(statement: str) -> Dict:
    def prepare_row(row: Dict, lang: str) -> Dict:
        result = {}
        for field in row:
            value = row[field]['value']
            if field in ('flag', 'coat_of_arms'):
                response = requests.head(value, allow_redirects=True)
                result[field] = response.url
            elif field == 'area':
                result[field] = str(int(float(value)))
            elif field.startswith('capital'):
                if 'capital' not in result:
                    result['capital'] = {}
                key = field.split('_')[1]
                if key == 'id':
                    result['capital'][key] = value.split('/')[-1]
                    links = get_links(result['capital'][key])
                    result['capital']['wiki'] = links[lang]['wiki']
                elif key in ('lat', 'lon'):
                    result['capital'][key] = float(value)
                else:
                    result['capital'][key] = value
                """
            if field == 'flag':
                png_name = 'flags/' + results[field]['value'].split('/')[-1].replace('svg', 'png')
                png_path = default_storage.path(png_name)
                PNGSurface.convert(url=results[field]['value'], write_to=png_path)
                result[field] = default_storage.url(png_name)
                """
            else:
                result[field] = value
        return result

    sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
    sparql.setQuery(statement)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {}
    for row in results:
        lang = row.pop('lang')['value']
        result[lang] = prepare_row(row, lang)
    return result


def query_by_wikidata_id(country_id: str, item_id: str) -> Dict:
    def statement_by_instance(country_id: str, item_id: str) -> str:
        return STATEMENT.format(item_id='wd:{}'.format(item_id), country_id=country_id, select='', condition='')

    result = query(statement_by_instance(country_id=country_id, item_id=item_id))
    links = get_links(item_id)
    for lang in result:
        links[lang].update(result[lang])
    return links


def query_by_name(country_id: str, name: str, language: str) -> Dict:
    def statement_by_name(country_id: str, name: str, language: str) -> str:
        condition = '?instance ?label "{name}"@{language}.'.format(name=name, language=language)
        return STATEMENT.format(item_id='?instance', country_id=country_id, select='?instance', condition=condition)

    result = query(statement_by_name(country_id=country_id, name=name, language=language))
    links = result
    if 'en' in result and 'instance' in result['en']:
        links = get_links(result['en']['instance'].split('/')[-1])
        for lang in result:
            links[lang].update(result[lang])
    return links
