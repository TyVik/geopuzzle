from typing import TypedDict, Dict, List, Literal

from django.core.handlers.wsgi import WSGIRequest

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


LanguageEnumType = Literal['en', 'ru']


class Point(TypedDict):
    lat: float
    lng: float


class GameQuestions(TypedDict):
    questions: List[Dict]
    solved: List[Dict]


class WSGILanguageRequest(WSGIRequest):
    LANGUAGE_CODE: str
