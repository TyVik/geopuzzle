'use strict';
/* global google */
import React from "react";
import {connect} from "react-redux";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";
import {showInfobox, PUZZLE_CHECK} from "../../actions";


class Polygon extends GooglePolygon {
    getBounds() {
        return this.state[_constants.POLYGON].getBounds();
    }

    getCenter() {
        return this.state[_constants.POLYGON].getBounds().getCenter();
    }

    componentDidMount() {
        google.maps.event.addListener(this.state[_constants.POLYGON], 'dragend', () => {
            let coords = JSON.parse(JSON.stringify(this.getBounds()));
            this.props.dispatch({type: PUZZLE_CHECK, coords: coords, id: this.props.id, ws: true, zoom: window.__MAP__.zoom});
        });
        google.maps.event.addListener(this.state[_constants.POLYGON], 'click', () => {
            if (!this.props.draggable) {
                this.props.dispatch(showInfobox(this.props));
            }
        });
    }
}


export default connect((state, ownProps) => {
    return state.polygons.find(x => x.id === ownProps.options.id);
})(Polygon);
