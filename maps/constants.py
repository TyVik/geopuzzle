from dataclasses import dataclass
from typing import List, TypedDict

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


@dataclass
class IndexPageGame:
    image: str
    slug: str
    name: str


@dataclass
class IndexPageGameType:
    world: List[IndexPageGame]
    parts: List[IndexPageGame]
    countries: List[IndexPageGame]


class InitGameMapOptions(TypedDict):
    streetViewControl: bool
    mapTypeControl: bool


class InitGameParams(TypedDict):
    zoom: Zoom
    center: Point
    options: InitGameMapOptions
