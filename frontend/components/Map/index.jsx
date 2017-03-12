'use strict';
import React from 'react';
import { connect } from 'react-redux'
import {getCountries} from '../../actions';
import GoogleMap from './GoogleMap';


class MapContainer extends React.Component {
    handleMapLoad = this.handleMapLoad.bind(this);

    handleMapLoad(map) {
        this._mapComponent = map;
        if (map) {
            this.props.dispatch(getCountries());
        }
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

    render() {
        return <GoogleMap {...this.props}
            containerElement={<div style={{height: window.innerHeight - 50, marginTop: '-20px'}}/>}
            mapElement={<div style={{height: '100%', margin: 0, padding: 0}} id="map"/>}
            onMapLoad={this.handleMapLoad}
            polygons={this.preparePolygons(this.props.polygons)}
            marker={this.props.marker}
        />
    }
}


export default connect(state => {
    let result = {...state.map, polygons: state.polygons};
    if (state.infobox.capital) {
        result.marker = {
            key: state.infobox.capital.name,
            defaultAnimation: 2,
            position: {
                lat: state.infobox.capital.lat,
                lng: state.infobox.capital.lon
            }
        }
    }
    return result;
})(MapContainer);
