"""Provides utility functions for encoding and decoding linestrings using the
Google encoded polyline algorithm.
"""
import math
from typing import Tuple, List, Union, Iterable, Optional

from django.contrib.gis.geos import MultiPolygon, Polygon

Point = Tuple[float, float]
PointList = Tuple[Point, ...]


def encode_coords(coords: PointList) -> str:
    """Encodes a polyline using Google's polyline algorithm

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    for more information.

    :param coords: Coordinates to transform (list of tuples in order: latitude,
    longitude).
    :type coords: list
    :returns: Google-encoded polyline string.
    :rtype: string
    """

    result = []

    prev_lat = 0
    prev_lng = 0

    for x, y in coords:
        lat, lng = int(y * 1e5), int(x * 1e5)

        d_lat = _encode_value(lat - prev_lat)
        d_lng = _encode_value(lng - prev_lng)

        prev_lat, prev_lng = lat, lng

        result.append(d_lat)
        result.append(d_lng)

    return ''.join(c for r in result for c in r)


def _split_into_chunks(value: int) -> Iterable[int]:
    while value >= 32:  # 2^5, while there are at least 5 bits

        # first & with 2^5-1, zeros out all the bits other than the first five
        # then OR with 0x20 if another bit chunk follows
        yield (value & 31) | 0x20
        value >>= 5
    yield value


def _encode_value(value: int) -> Iterable[str]:
    # Step 2 & 4
    value = ~(value << 1) if value < 0 else (value << 1)

    # Step 5 - 8
    chunks = _split_into_chunks(value)

    # Step 9-10
    return (chr(chunk + 63) for chunk in chunks)


def decode(point_str: str) -> List[Point]:
    """Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a generic method that returns a list of (latitude, longitude)
    tuples.

    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list

    """

    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks: List[List[int]] = [[]]
    for char in point_str:

        # convert each character to decimal from ascii
        value = ord(char) - 63

        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)
        value &= 0x1F

        coord_chunks[-1].append(value)

        if split_after:
            coord_chunks.append([])

    del coord_chunks[-1]

    coords: List[float] = []

    for coord_chunk in coord_chunks:
        coord = 0

        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)

            # there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord  # invert
        coord >>= 1
        coords.append(coord / 100000.0)

    # convert the 1 dimensional list to a 2 dimensional list and offsets to
    # actual values
    points = []
    prev_x = 0.0
    prev_y = 0.0
    for i in range(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue

        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when
        # they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))

    return points


def encode_geometry(polygon: Union[Polygon, MultiPolygon], min_points: Optional[int] = None) -> List[str]:
    def encode_part(subpolygon: Polygon) -> List[str]:
        subpart = [encode_coords(subpolygon.coords[0])]
        if len(subpolygon.coords) > 1:
            subpart.append(encode_coords(subpolygon.coords[1]))
        return subpart

    result: List[str] = []
    if isinstance(polygon, MultiPolygon):
        for part in polygon:
            if min_points is not None and part.num_points < min_points:
                continue
            result += encode_part(part)
    else:
        result += encode_part(polygon)
    return result if len(result) > 0 else encode_geometry(polygon)


def normalize_polygon(polygon: Union[Polygon, MultiPolygon], precision) -> Union[Polygon, MultiPolygon]:
    def normalize_subpolygon(subpolygon: Polygon) -> Tuple[PointList, ...]:
        def process(coords: PointList) -> List[Point]:
            result = [coords[0]]
            for coord in coords:
                prev = result[-1]
                delta = (math.trunc(coord[0] - prev[0]), math.trunc(coord[1] - prev[1]))
                steps = max(abs(delta[0]), abs(delta[1]))
                if steps > 1:
                    delta_coord = (delta[0] * 0.4 / steps, delta[1] * 0.4 / steps)
                    for _ in range(steps):
                        prev = result[-1]
                        result.append((prev[0] + delta_coord[0], prev[1] + delta_coord[1]))
                result.append(coord)
            return result

        result = [process(subpolygon.coords[0])]
        if len(subpolygon.coords) > 1:
            result.append(process(subpolygon.coords[1]))
        return tuple(result)

    result = polygon.simplify(precision, preserve_topology=True)
    if isinstance(result, MultiPolygon):
        subpolygons = []
        for part in result:
            subpolygons.append(Polygon(*normalize_subpolygon(part)))
        result = MultiPolygon(*subpolygons)
    else:
        result = Polygon(*normalize_subpolygon(result))
    return result
