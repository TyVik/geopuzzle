'use strict';
import React from 'react';
import GoogleMap from './GoogleMap';
import { decodePolygon } from "../utils";
import { getColors } from "../constants";


class MapContainer extends React.Component {
  constructor(props) {
    super(props);
    this.mapLoaded = false;
    this.colors = getColors();
  }

  static preparePolygon = (polygon, useDecode = true) => {
    if (useDecode) {
      return decodePolygon(polygon);
    } else {
      return polygon;
    }
  };

  static moveTo(paths, fromLatLng, toLatLng) {
    const from = new google.maps.LatLng(fromLatLng[1], fromLatLng[0]);
    const to = new google.maps.LatLng(toLatLng[1], toLatLng[0]);
    let newPoints =[];
    let newPaths = [];

    for (let p = 0; p < paths.length; p++) {
      let path = paths[p];
      newPoints.push([]);

      for (let i = 0; i < path.length; i++) {
        newPoints[newPoints.length-1].push({
          heading: google.maps.geometry.spherical.computeHeading(from, path[i]),
          distance: google.maps.geometry.spherical.computeDistanceBetween(from, path[i])
        });
      }
    }

    for (let j = 0, jl = newPoints.length; j < jl; j++) {
      let shapeCoords = [];
      let relativePoint = newPoints[j];
      for (let k = 0, kl = relativePoint.length; k < kl; k++) {
        shapeCoords.push(google.maps.geometry.spherical.computeOffset(to, relativePoint[k].distance, relativePoint[k].heading));
      }
      newPaths.push(shapeCoords);
    }
    return newPaths;
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
      this.props.mapClick(e.latLng.lat(), e.latLng.lng());
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
      let color = polygon.isSolved ? this.colors.SOLVED : this.colors.WRONG;
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
    let props = {...this.props};
    if (!props.showMap) {
      return null;
    }
    return <GoogleMap {...props}
                      containerElement={<div style={{height: '100%'}}/>}
                      mapElement={<div style={{height: '100%', margin: 0, padding: 0}} id="map"/>}
                      onMapLoad={this.handleMapLoad}
                      onMapClick={this.handleMapClick}
                      regions={this.preparePolygons(props.regions)}
                      marker={this.showMarker(props.infobox)}
    />;
  }
}


export default MapContainer;