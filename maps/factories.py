import string

import factory
from django.conf import settings
from django.contrib.gis.geos import Point,  MultiPolygon,  Polygon
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyInteger

from maps.models import Region, RegionTranslation

POINTS = (
    ([-2.4610019, 49.4612907], [-2.4610233, 49.4613325], [-2.4628043, 49.4608862], [-2.4634051, 49.4606073], [-2.4640274, 49.4606491], [-2.4642205, 49.4599378], [-2.4651432, 49.4597984], [-2.4651861, 49.4587523], [-2.4658513, 49.4584455], [-2.4653149, 49.4574273], [-2.4653149, 49.4564509], [-2.4643064, 49.4562138], [-2.4639845, 49.4557954], [-2.4626756, 49.4559349], [-2.462461, 49.4563533], [-2.4618816, 49.4569531], [-2.4607658, 49.456967], [-2.46068, 49.4574691], [-2.4605298, 49.4577063], [-2.46068, 49.4578178], [-2.460444, 49.4580828], [-2.4600363, 49.4579434], [-2.4595642, 49.4580828], [-2.4595213, 49.4583339], [-2.4594784, 49.458836], [-2.4592209, 49.4590452], [-2.4592209, 49.4593242], [-2.4590921, 49.4595055], [-2.4593067, 49.4597147], [-2.4596715, 49.4599239], [-2.45965, 49.4602168], [-2.4598861, 49.4603981], [-2.4602509, 49.4604678], [-2.4603367, 49.460677], [-2.4608088, 49.4609002], [-2.4610019, 49.4612907]), 
    ([-2.4636197, 49.4623646], [-2.4636412, 49.4626086], [-2.4640059, 49.4627411], [-2.4646497, 49.4634384], [-2.4650359, 49.4632292], [-2.4655938, 49.4631734], [-2.4655402, 49.462769], [-2.4655831, 49.4624761], [-2.4647677, 49.4621205], [-2.4640918, 49.4624831], [-2.4636197, 49.4623646]) 
)
INFOBOX = {
    "area": "178",
    "flag": "Flag_of_Aruba.svg",
    "name": "Aruba",
    "wiki": "https://en.wikipedia.org/wiki/Aruba",
    "capital": {
        "id": "Q131243",
        "lat": 12.516,
        "lon": -70.033,
        "name": "Oranjestad",
        "wiki": "https://en.wikipedia.org/wiki/Oranjestad,_Aruba"
    },
    "geonamesID": "3577279",
    "population": "102911",
    "coat_of_arms": "Coat_of_arms_of_Aruba.svg"
}


def multipolygon_factory():
    return MultiPolygon(*(Polygon(points) for points in POINTS))


class GameFactory(DjangoModelFactory):
    is_published = True
    center = Point(0,  0)
    zoom = 3
    slug = FuzzyText(chars=string.ascii_lowercase)


class RegionFactory(DjangoModelFactory):
    title = FuzzyText()
    polygon = MultiPolygon(*(Polygon(points) for points in POINTS))
    osm_id = FuzzyInteger(low=1, high=65535)

    class Meta:
        model = Region

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        for lang in settings.ALLOWED_LANGUAGES:
            RegionTranslation.objects.create(
                language_code=lang, master=self, name=f'{self.title}-{lang}', infobox=INFOBOX)
