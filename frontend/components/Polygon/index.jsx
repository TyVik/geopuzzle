/* global google */
import React from "react";
import {connect} from "react-redux";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";
import {dragEndPolygon} from "../../actions";


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
            this.props.dispatch(dragEndPolygon(this));
        });
    }
}


const mapStateToProps = (state, ownProps) => {
    return state.map.polygons.find(x => x.id === ownProps.options.id);
};

export default connect(mapStateToProps)(Polygon);
