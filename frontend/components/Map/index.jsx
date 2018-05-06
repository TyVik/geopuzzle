'use strict';
import React from 'react';
import GoogleMap from './GoogleMap';


class MapContainer extends React.Component {
    handleMapLoad = (map) => {
        this._mapComponent = map;
        if (map && this.props.initCallback) {
            this.props.initCallback(map);
        }
    };

    handleMapClick = (e) => {
        this.props.mapClick(e);
    };

    preparePolygons(polygons) {
        return polygons.map(polygon => {
            return {
                map: this._mapComponent,
                options: {
                    strokeColor: polygon.isSolved ? '#419641' : '#d9534f',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: polygon.isSolved ? '#419641' : '#d9534f',
                    fillOpacity: 0.35,
                    geodesic: true,
                    draggable: polygon.draggable,
                    zIndex: polygon.draggable ? 2 : 1,
                    paths: polygon.paths,
                    id: polygon.id,
                },
                onClick: this.props.onPolygonClick,
                onDragPolygon: this.props.onDragPolygon
            };
        });
    }

    showMarker(infobox) {
        if (infobox && infobox.capital) {
            return {
                key: infobox.capital.name,
                defaultAnimation: 2,
                position: {
                    lat: infobox.capital.lat,
                    lng: infobox.capital.lon
                }
            }
        }
    }

    render() {
        let props = {...this.props, ...window.__MAP__, mapTypeId: this.props.mapTypeId};
        return <GoogleMap {...props}
            containerElement={<div style={{height: '100%'}}/>}
            mapElement={<div style={{height: '100%', margin: 0, padding: 0}} id="map"/>}
            onMapLoad={this.handleMapLoad}
            onMapClick={this.handleMapClick}
            polygons={this.preparePolygons(this.props.regions)}
            marker={this.showMarker(this.props.infobox)}
        />
    }
}


export default MapContainer;
