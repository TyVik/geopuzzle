'use strict';
/* global google */
import React from "react";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";


class Polygon extends GooglePolygon {
    getBounds() {
        return this.state[_constants.POLYGON].getBounds();
    }

    getPaths() {
        return this.state[_constants.POLYGON].getPaths();
    }

    componentDidMount() {
        google.maps.event.addListener(this.state[_constants.POLYGON], 'dragend', () => {
            this.props.onDragPolygon(this.props.options.id, this.getBounds(), this.getPaths());
        });
        google.maps.event.addListener(this.state[_constants.POLYGON], 'click', () => {
            this.props.onClick(this.props.options);
        });
    }
}


export default Polygon;
