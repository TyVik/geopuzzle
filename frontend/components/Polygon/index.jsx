'use strict';
/* global google */
import React from "react";
import {connect} from "react-redux";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";
import {showInfobox, DRAG_END_POLYGON, DRAG_END_POLYGON_FAIL} from "../../actions";


class Polygon extends GooglePolygon {
    isBounded() {
        let paths = this.getPaths().getArray();
        for (let i = 0; i < paths.length; i++) {
            let p = paths[i].getArray();
            for (let j = 0; j < p.length; j++) {
                if (!this.props.answer.contains(p[j])) {
                    return false;
                }
            }
        }
        return true;
    }

    getPaths() {
        return this.state[_constants.POLYGON].getPaths();
    }

    componentDidMount() {
        google.maps.event.addListener(this.state[_constants.POLYGON], 'dragend', () => {
            if (this.isBounded()) {
                this.props.dispatch({type: DRAG_END_POLYGON, id: this.props.id});
                this.props.dispatch(showInfobox(this.props));
            } else {
                this.props.dispatch({type: DRAG_END_POLYGON_FAIL, id: this.props.id, paths: this.getPaths()});
            }
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
