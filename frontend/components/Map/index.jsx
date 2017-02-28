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
                    strokeColor: polygon.draggable ? '#FF0000' : '#00FF00',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: polygon.draggable ? '#FF0000' : '#00FF00',
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
        return <GoogleMap
            zoom={this.props.zoom}
            center={this.props.center}
            containerElement={<div style={{height: `500px`}}/>}
            mapElement={<div style={{height: `500px`}} id="map"/>}
            onMapLoad={this.handleMapLoad}
            polygons={this.preparePolygons(this.props.polygons)}
        />
    }
}


export default connect(state => (state.map))(MapContainer);
