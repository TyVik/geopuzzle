var map;
var puzzle = [];

function addCountries(position) {
    var options = {
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        geodesic: true,
        map: map,
        draggable: true,
        zIndex: 2,
    };
  for (var i = countries.length - 1; i >= 0; i--) {
    var country = new google.maps.Polygon(options);
    country.polygon = countries[i];
    country.answer = answers[i];
    country.setPaths(country.pathMultipolygonToArray(country.polygon));
    google.maps.event.addListener(country, 'dragend', function() {
        if (this.boundsContains()) {
            this.replacePiece();
        }
    });
    country.moveTo(new google.maps.LatLng(position[0], position[1]));
    puzzle.push(country);
    country = null;
  };
}

function initialize(zoom, center, default_position) {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoom,
        center: new google.maps.LatLng(center[0], center[1]),
        mapTypeId: google.maps.MapTypeId.SATELLITE,
        streetViewControl: true,
    });
    addCountries(default_position);
}

function giveUp() {
  for (var i = puzzle.length - 1; i >= 0; i--) {
    puzzle[i].replacePiece();
  };
}

function reload() {
  location.reload();
}

function debugAnswers() {
  for (var i = answers.length - 1; i >= 0; i--) {
    rect = new google.maps.Rectangle({map: map});
    rect.setBounds(answers[i]);
  }
}