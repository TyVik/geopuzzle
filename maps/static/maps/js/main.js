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
    var counter = document.getElementById('counter_total');
    counter.innerText = geodata.length;

    geodata.forEach(function(item, i, arr) {
        var country = new google.maps.Polygon(options);
        country.id = item.id;
        country.polygon = item.polygon;
        country.answer = new google.maps.LatLngBounds(
                new google.maps.LatLng(item.answer[0][1], item.answer[0][0]),
                new google.maps.LatLng(item.answer[1][1], item.answer[1][0])
            );
        country.setPaths(country.pathStringsToArray(country.polygon));
        google.maps.event.addListener(country, 'dragend', function() {
            if (this.boundsContains()) {
                this.replacePiece();
                this.showInfobox();
            }
        });
        country.moveTo(new google.maps.LatLng(position[1], position[0]));
        puzzle.push(country);
        country = null;
    });
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

function close_infobox() {
    var wrap_infobox = document.getElementById('wrap_infobox');
    wrap_infobox.style.display = 'none';
}

function resizeWrapper() {
    var map_wrapper = document.querySelector('#map_wrapper');
    map_wrapper.style.height = (window.innerHeight - 110) + 'px';
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: init.zoom,
        center: new google.maps.LatLng(init.center[1], init.center[0]),
        mapTypeId: google.maps.MapTypeId.TERRAIN,
        streetViewControl: true,
    });
    addCountries(init.position);
}

window.onload = resizeWrapper;