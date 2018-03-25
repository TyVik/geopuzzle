'use strict';
/* global google */
import {SET_MAP_TYPE} from "../actions";


let init_map = {
    ...window.__MAP__,
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    options: {
        streetViewControl: false,
        mapTypeControl: false
    }
};

const map = (state = {...init_map}, action) => {
    switch (action.type) {
        case SET_MAP_TYPE:
            return {...state, mapTypeId: action.value};
        default:
            return state
    }
};


export default map;
