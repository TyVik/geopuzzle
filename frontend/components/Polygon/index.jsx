'use strict';
/* global google */
import React from "react";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";


class Polygon extends GooglePolygon {
    getBounds() {
        return this.state[_constants.POLYGON].getBounds();
    }

    componentDidMount() {
        google.maps.event.addListener(this.state[_constants.POLYGON], 'dragend', () => {
            let coords = JSON.parse(JSON.stringify(this.getBounds()));
            this.props.onDragEnd(this.getBounds(), this.props.options.id);
            // this.props.dispatch({type: PUZZLE_CHECK, coords: coords, id: this.props.id, ws: true, zoom: window.__MAP__.zoom});
        });
        google.maps.event.addListener(this.state[_constants.POLYGON], 'click', () => {
            this.props.onClick(this.props.options);
        });
    }
}


export default Polygon;
