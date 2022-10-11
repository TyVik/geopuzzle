/**
 * Polygon getBounds extension - google-maps-extensions
 * @see http://code.google.com/p/google-maps-extensions/source/browse/google.maps.Polygon.getBounds.js
 */
if (!google.maps.Polygon.prototype.getBounds) {
    google.maps.Polygon.prototype.getBounds = function(_latLng) {
        const bounds = new google.maps.LatLngBounds();
        const paths = this.getPaths();
        let path;

        for (let p = 0; p < paths.getLength(); p++) {
            path = paths.getAt(p);
            for (let i = 0; i < path.getLength(); i++) {
                bounds.extend(path.getAt(i));
            }
        }

        return bounds;
    };
}
