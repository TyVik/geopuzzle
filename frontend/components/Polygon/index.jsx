'use strict';
/* global google */
import React from "react";
import {connect} from "react-redux";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";
import {showInfobox, DRAG_END_POLYGON, DRAG_END_POLYGON_FAIL} from "../../actions";


class Polygon extends GooglePolygon {
    getPaths() {
        return this.state[_constants.POLYGON].getPaths();
    }

    getCenter() {
        return this.state[_constants.POLYGON].getBounds().getCenter();
    }

    componentDidMount() {
        google.maps.event.addListener(this.state[_constants.POLYGON], 'dragend', () => {
            let formData = new FormData();
            let latLng = this.getCenter();
            formData.append('lat', latLng.lat());
            formData.append('lng', latLng.lng());
            let options = {
                method: 'POST',
                body: formData
            };
            this.props.dispatch((dispatch) =>
                fetch('//' + location.host + '/puzzle/' + this.props.id + '/check/', options)
                    .then(response => response.json())
                    .then(json => {
                        if (json.success) {
                            return dispatch({...json, type: DRAG_END_POLYGON, id: this.props.id})
                        } else {
                            return dispatch({type: DRAG_END_POLYGON_FAIL, id: this.props.id, paths: this.getPaths()});
                        }
                    })
                    .catch(response => {
                        return {type: DRAG_END_POLYGON_FAIL, id: this.props.id, paths: this.getPaths()};
                    })
            );
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
