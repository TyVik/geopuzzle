import json
import logging
from typing import Dict

from urllib.request import urlopen, unquote
# from cairosvg.surface import PNGSurface
import requests
from SPARQLWrapper import JSON
from SPARQLWrapper import SPARQLWrapper
from django.conf import settings
from django.contrib.gis.geos import Point, GEOSGeometry
from django.template.loader import render_to_string


fetch_logger = logging.getLogger('fetch_region')


def get_links(instance: str) -> Dict:
    result = {x: {} for x in settings.ALLOWED_LANGUAGES}
    url = 'http://www.wikidata.org/entity/{}'.format(instance)
    response = urlopen(url).read().decode('utf8')
    response = json.loads(response)
    for lang in result:
        try:
            links = response['entities'][instance]['sitelinks']['{}wiki'.format(lang)]
            result[lang]['wiki'] = unquote(links['url'], 'utf-8')
            result[lang]['name'] = links['title']
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
                    result['capital']['wiki'] = links[lang].get('wiki', '')
                elif key == 'coord':
                    point = GEOSGeometry(value)
                    result['capital']['lon'] = point.x
                    result['capital']['lat'] = point.y
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

    sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql", agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    sparql.setQuery(statement + '')  # convert SafeText -> str
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader('Accept', 'application/json')
    results = sparql.query().convert()
    results = results['results']['bindings']
    result = {}
    for row in results:
        lang = row.pop('lang')['value']
        result[lang] = prepare_row(row, lang)
    return result


def query_by_wikidata_id(template: str, context: dict) -> Dict:
    query_text = render_to_string(template, context=context)
    result = query(str(query_text))
    links = get_links(context['item_id'])
    for lang in result:
        links[lang].update(result[lang])
    return links
