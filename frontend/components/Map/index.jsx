'use strict';
import React from 'react';
import GoogleMap from './GoogleMap';


let COLORS = {
  SOLVED: '#419641',
  WRONG: '#d9534f',
  UNKNOWN: '#ffffff',
};

class MapContainer extends React.Component {
  constructor(props) {
    super(props);
    this.mapLoaded = false;
  }

  handleMapLoad = (map) => {
    this._mapComponent = map;
    // load regions from server only at the first time
    if (map && this.props.initCallback && !this.mapLoaded) {
      this.mapLoaded = true;
      this.props.initCallback(map);
    }
  };

  handleMapClick = (e) => {
    if (this.props.mapClick !== undefined) {
      this.props.mapClick(e);
    }
  };

  commonOptions(shape, color) {
    return {
      map: this._mapComponent,
      options: {
        strokeColor: color,
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: color,
        fillOpacity: 0.35,
        geodesic: true,
        id: shape.id,
      },
      onClick: this.props.onPolygonClick,
      onDragPolygon: this.props.onDragPolygon
    };
  }

  preparePolygons(polygons) {
    if (!polygons) {
      return [];
    }
    return polygons.map(polygon => {
      let color = polygon.isSolved ? COLORS.SOLVED : COLORS.WRONG;
      let result = this.commonOptions(polygon, color);
      result.key = `${polygon.draggable}${polygon.id}`;
      result.options.draggable = polygon.draggable;
      result.options.zIndex = polygon.draggable ? 2 : 1;
      result.paths = polygon.paths;
      return result;
    });
  }

  showMarker(infobox) {
    if (infobox) {
      return {
        key: 'center',
        defaultAnimation: 2,
        position: {
          lat: infobox.marker.lat,
          lng: infobox.marker.lng
        }
      }
    }
  }

  render() {
    let props = {...this.props, ...this.props.map, mapTypeId: this.props.mapTypeId};
    if (!this.props.showMap) {
      return null;
    }
    return <GoogleMap {...props}
                      containerElement={<div style={{height: '100%'}}/>}
                      mapElement={<div style={{height: '100%', margin: 0, padding: 0}} id="map"/>}
                      onMapLoad={this.handleMapLoad}
                      onMapClick={this.handleMapClick}
                      polygons={this.preparePolygons(this.props.regions)}
                      marker={this.showMarker(this.props.infobox)}
    />;
  }
}


export default MapContainer;
