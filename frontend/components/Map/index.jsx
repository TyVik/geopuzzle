'use strict';
import React from 'react';
import { connect } from 'react-redux'
import GoogleMap from './GoogleMap';


class MapContainer extends React.Component {
    handleMapLoad = this.handleMapLoad.bind(this);
    handleMapClick = this.handleMapClick.bind(this);

    handleMapLoad(map) {
        this._mapComponent = map;
        if (map) {
            this.props.dispatch(this.props.initCallback());
        }
    }

    handleMapClick(e) {
        this.props.dispatch(this.props.mapClick(e));
    }

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
                }
            };
        });
    }

    showMarker(infobox) {
        if (infobox.capital) {
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
        return <GoogleMap {...this.props}
            containerElement={<div style={{height: window.innerHeight - 50, marginTop: '-20px'}}/>}
            mapElement={<div style={{height: '100%', margin: 0, padding: 0}} id="map"/>}
            onMapLoad={this.handleMapLoad}
            onMapClick={this.handleMapClick}
            polygons={this.preparePolygons(this.props.polygons)}
            marker={this.showMarker(this.props.infobox)}
        />
    }
}


export default connect(state => {
    return {...state.map, polygons: state.polygons, infobox: state.infobox};
})(MapContainer);
