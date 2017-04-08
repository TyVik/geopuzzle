/**
 * google.maps.Polygon.moveTo() — Move a Polygon on Google Maps V3 to a new LatLng()
 * Built by Bramus! - http://www.bram.us/
 *
 * @requires  google.maps.Polygon.getBounds
 * @requires  google.maps.geometry
 */
if (!google.maps.Polygon.prototype.moveTo) {
    google.maps.Polygon.prototype.moveTo = function(from, latLng) {

        // our vars
        var boundsCenter = from, // center of the polygonbounds
            paths = this.getPaths(), // paths that make up the polygon
            newPoints =[], // array on which we'll store our new points
            newPaths = []; // array containing the new paths that make up the polygon

        // geodesic enabled: we need to recalculate every point relatively
        if (this.geodesic) {

            // loop all the points of the original path and calculate the bearing + distance of that point relative to the center of the shape
            for (var p = 0; p < paths.getLength(); p++) {
                path = paths.getAt(p);
                newPoints.push([]);

                for (var i = 0; i < path.getLength(); i++) {
                    newPoints[newPoints.length-1].push({
                        heading: google.maps.geometry.spherical.computeHeading(boundsCenter, path.getAt(i)),
                        distance: google.maps.geometry.spherical.computeDistanceBetween(boundsCenter, path.getAt(i))
                    });
                }
            }

            // now that we have the "relative" points, rebuild the shapes on the new location around the new center
            for (var j = 0, jl = newPoints.length; j < jl; j++) {
                var shapeCoords = [],
                    relativePoint = newPoints[j];
                for (var k = 0, kl = relativePoint.length; k < kl; k++) {
                    shapeCoords.push(google.maps.geometry.spherical.computeOffset(
                        latLng,
                        relativePoint[k].distance,
                        relativePoint[k].heading
                    ));
                }
                newPaths.push(shapeCoords);
            }

        }

        // geodesic not enabled: adjust the coordinates pixelwise
        else {

            var latlngToPoint = function(map, latlng){
                var normalizedPoint = map.getProjection().fromLatLngToPoint(latlng); // returns x,y normalized to 0~255
                var scale = Math.pow(2, map.getZoom());
                var pixelCoordinate = new google.maps.Point(normalizedPoint.x * scale, normalizedPoint.y * scale);
                return pixelCoordinate;
            };
            var pointToLatlng = function(map, point){
                var scale = Math.pow(2, map.getZoom());
                var normalizedPoint = new google.maps.Point(point.x / scale, point.y / scale);
                var latlng = map.getProjection().fromPointToLatLng(normalizedPoint);
                return latlng;
            };

            // calc the pixel position of the bounds and the new latLng
            var boundsCenterPx = latlngToPoint(this.map, boundsCenter),
                latLngPx = latlngToPoint(this.map, latLng);

            // calc the pixel difference between the bounds and the new latLng
            var dLatPx = (boundsCenterPx.y - latLngPx.y) * (-1),
                dLngPx = (boundsCenterPx.x - latLngPx.x) * (-1);

            // adjust all paths
            for (var p = 0; p < paths.getLength(); p++) {
                path = paths.getAt(p);
                newPaths.push([]);
                for (var i = 0; i < path.getLength(); i++) {
                    var pixels = latlngToPoint(this.map, path.getAt(i));
                    pixels.x += dLngPx;
                    pixels.y += dLatPx;
                    newPaths[newPaths.length-1].push(pointToLatlng(this.map, pixels));
                }
            }

        }

        // Update the path of the Polygon to the new path
        this.setPaths(newPaths);

        // Return the polygon itself so we can chain
        return this;

    };
}