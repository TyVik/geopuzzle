'use strict';
/* global google */
import React from "react";
import {Polygon as GooglePolygon} from "react-google-maps";
import * as _constants from "react-google-maps/lib/constants";


class Polygon extends GooglePolygon {
    getBounds() {
        return this.state[_constants.POLYGON].getBounds();
    }
}

export default Polygon;
