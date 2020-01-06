import logging
from typing import Dict, TypedDict
from urllib.parse import unquote

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.template.loader import render_to_string

from common.constants import LanguageEnumType

fetch_logger = logging.getLogger('fetch_region')


class LinkDict(TypedDict):
    wiki: str
    name: str


class CapitalDict(TypedDict):
    id: str
    wiki: str
    lat: float
    lon: float
    name: str


class InfoboxDict(TypedDict):
    name: str
    geonamesID: str
    area: str
    flag: str
    coat_of_arms: str
    population: str
    capital: CapitalDict
    wiki: str


class Wikidata:
    def __init__(self, wikidata_id: int):
        self.wikidata_id = wikidata_id

    @staticmethod
    def get_links(instance: str) -> Dict[LanguageEnumType, LinkDict]:
        result: Dict[LanguageEnumType, LinkDict] = {x: {'wiki': '', 'name': ''} for x in settings.ALLOWED_LANGUAGES}
        response = requests.get(f'http://www.wikidata.org/entity/{instance}')
        data = response.json()
        for lang in result:
            try:
                links = data['entities'][instance]['sitelinks'][f'{lang}wiki']
                result[lang]['wiki'] = unquote(links['url'], 'utf-8')
                result[lang]['name'] = links['title']
            except:
                fetch_logger.warning('Links to wiki for %s (%s) are empty', instance, lang)
        return result

    def prepare_row(self, row: Dict, lang: LanguageEnumType) -> InfoboxDict:
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
                    links = self.get_links(result['capital'][key])
                    result['capital']['wiki'] = links[lang].get('wiki', '')
                elif key == 'coord':
                    point = GEOSGeometry(value)
                    result['capital']['lon'] = point.x
                    result['capital']['lat'] = point.y
                else:
                    result['capital'][key] = value
            else:
                result[field] = value
        return result

    @staticmethod
    def query(statement: str) -> Dict:
        sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql",
                               agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        sparql.setQuery(statement + '')  # convert SafeText -> str
        sparql.setReturnFormat(JSON)
        sparql.addCustomHttpHeader('Accept', 'application/json')
        results = sparql.query().convert()
        return results['results']['bindings']

    def query_by_wikidata_id(self, template: str, context: dict):
        query_text = render_to_string(template, context=context)
        raw = self.query(str(query_text))
        wiki = {}
        for row in raw:
            lang = row.pop('lang')['value']
            wiki[lang] = self.prepare_row(row, lang)

        links = self.get_links(context['item_id'])
        return {lang: {**wiki.get(lang, {}), **links[lang]} for lang in settings.ALLOWED_LANGUAGES}

    def get_infoboxes(self, parent_id: int) -> Dict[LanguageEnumType, dict]:
        fetch_logger.info(f'Get infobox: {self.wikidata_id}')
        return self.query_by_wikidata_id('wikidata/regions.txt', {'country_id': parent_id, 'item_id': self.wikidata_id})
