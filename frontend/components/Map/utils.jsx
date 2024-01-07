/* global google */


function decodePolygon(polygon) {
  return polygon.map(polygon => (google.maps.geometry.encoding.decodePath(polygon)));
}

export { decodePolygon };
