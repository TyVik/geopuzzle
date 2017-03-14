'use strict';
/* global google */
import {INIT_LOAD, INIT_LOAD_FAIL, INIT_PUZZLE_DONE, SET_MAP_TYPE, INIT_QUIZ_DONE} from "../actions";


let init_map = {
    ...window.__MAP__,
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    options: {
        streetViewControl: false,
        mapTypeControl: false
    }
};

const map = (state = {...init_map, isLoaded: null}, action) => {
    switch (action.type) {
        case INIT_LOAD:
            return {...state, isLoaded: null};
        case INIT_LOAD_FAIL:
            return {...state, isLoaded: false};
        case INIT_QUIZ_DONE:
        case INIT_PUZZLE_DONE:
            return {...state, isLoaded: true};
        case SET_MAP_TYPE:
            return {...state, mapTypeId: action.value};
        default:
            return state
    }
};


export default map;
