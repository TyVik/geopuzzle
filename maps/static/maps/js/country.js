
if (!google.maps.Polygon.prototype.polygon) {
    google.maps.Polygon.prototype.polygon = "";
}

if (!google.maps.Polygon.prototype.answer) {
    google.maps.Polygon.prototype.answer = "";
}

if (!google.maps.Polygon.prototype.pathMultipolygonToArray) {
    google.maps.Polygon.prototype.pathMultipolygonToArray = function(multipolygon) {
        var result = [];
        _.each(multipolygon.coordinates, function(polygon) {
            result.push(_.map(polygon[0], function(point) {
                return new google.maps.LatLng(point[1], point[0]);
            }));
            result.push(_.map(polygon[1], function(point) {
                return new google.maps.LatLng(point[1], point[0]);
            }));
        });
        return result;
    }
}

if (!google.maps.Polygon.prototype.boundsContains) {
    google.maps.Polygon.prototype.boundsContains = function() {
        var paths = this.getPaths().getArray();
        for (var i = 0; i < paths.length; i++) {
            var p = paths[i].getArray();
            for (var j = 0; j < p.length; j++) {
                if (!this.answer.contains(p[j])) {
                    return false;
                }
            }
        }
        return true;
    }
}

if (!google.maps.Polygon.prototype.replacePiece) {
    google.maps.Polygon.prototype.replacePiece = function() {
        var options = {
            strokeColor: '#00FF00',
            fillColor: '#00FF00',
            draggable: false,
            zIndex: 1,
        };
        options.paths = this.pathMultipolygonToArray(this.polygon);
        this.setOptions(options);
    }
}

if (!google.maps.Polygon.prototype.showInfobox) {
    google.maps.Polygon.prototype.showInfobox = function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/maps/infobox/' + this.id + '/', true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if(xhr.status == 200) {
                    var counter = document.getElementById('counter_current');
                    counter.innerText = parseInt(counter.innerText, 10) + 1;
                    var infobox = document.getElementById('infobox');
                    infobox.innerHTML = xhr.responseText;
                    var wrap_infobox = document.getElementById('wrap_infobox');
                    wrap_infobox.style.display = 'inline-block';
                }
            }
        };
        xhr.send();
        return true;
    }
}
