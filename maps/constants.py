from typing import List, TypedDict, Optional

from django_enumfield import enum

from common.constants import Point


class Zoom(enum.Enum):
    WORLD = 3
    LARGE_COUNTRY = 4
    BIG_COUNTRY = 5
    COUNTRY = 6
    SMALL_COUNTRY = 7
    LITTLE_COUNTRY = 8
    REGION = 9


class IndexPageGame(TypedDict):
    id: int
    image: str
    name: str
    url: str
    user: str


class IndexPageGameType(TypedDict):
    world: List[IndexPageGame]
    parts: List[IndexPageGame]


class InitGameMapOptions(TypedDict):
    streetViewControl: bool
    mapTypeControl: bool


class InitGameParams(TypedDict):
    zoom: Zoom
    center: Point
    options: InitGameMapOptions


class GameData(TypedDict):
    name: str
    parts: str


class OsmRegionData(TypedDict):
    level: int
    boundary: str
    path: Optional[List[int]]
    alpha3: Optional[str]
    timezone: Optional[str]


GAMES = {
    'puzzle': ('puzzle', 'Puzzle'),
    'quiz': ('quiz', 'Quiz'),
}
