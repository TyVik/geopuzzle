from typing import TypedDict, Dict, List, Literal

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

LanguageEnumType = Literal['en', 'ru']
GameCategoryEnumType = Literal['puzzle', 'quiz']


class Point(TypedDict):
    lat: float
    lng: float


class GameQuestions(TypedDict):
    questions: List[Dict]
    solved: List[Dict]
