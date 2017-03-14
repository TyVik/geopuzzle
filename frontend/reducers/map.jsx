'use strict';
/* global google */
import {GET_COUNTRIES, GET_COUNTRIES_FAIL, GET_COUNTRIES_DONE, SET_MAP_TYPE, INIT_QUIZ_DONE, INIT_QUIZ_FAIL} from "../actions";


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
        case GET_COUNTRIES:
            return {...state, isLoaded: null};
        case INIT_QUIZ_FAIL:
        case GET_COUNTRIES_FAIL:
            return {...state, isLoaded: false};
        case INIT_QUIZ_DONE:
        case GET_COUNTRIES_DONE:
            return {...state, isLoaded: true};
        case SET_MAP_TYPE:
            return {...state, mapTypeId: action.value};
        default:
            return state
    }
};


export default map;
