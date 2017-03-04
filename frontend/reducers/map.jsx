/* global google */
import {GET_COUNTRIES, GET_COUNTRIES_FAIL, GET_COUNTRIES_DONE} from "../actions";


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
        case GET_COUNTRIES_FAIL:
            return {...state, isLoaded: false};
        case GET_COUNTRIES_DONE:
            return {...state, isLoaded: true};
        default:
            return state
    }
};


export default map;
