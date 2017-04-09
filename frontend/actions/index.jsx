'use strict';
import "whatwg-fetch";
import localization from "../localization";

export const NOOP = 'NOOP';
export const INIT_LOAD = 'INIT_LOAD';
export const INIT_LOAD_FAIL = 'INIT_LOAD_FAIL';

export const DRAG_END_POLYGON = 'DRAG_END_POLYGON';
export const SET_MAP_TYPE = 'SET_MAP_TYPE';
export const SHOW_CONGRATULATION = 'SHOW_CONGRATULATION';

export const GET_INFOBOX_DONE = 'GET_INFOBOX_DONE';
export const GET_INFOBOX_FAIL = 'GET_INFOBOX_FAIL';
export const SHOW_INFOBOX = 'SHOW_INFOBOX';
export const CLOSE_INFOBOX = 'CLOSE_INFOBOX';

export const PUZZLE_INIT_DONE = 'PUZZLE_INIT_DONE';
export const PUZZLE_CHECK = 'PUZZLE_CHECK';
export const PUZZLE_CHECK_SUCCESS = 'PUZZLE_CHECK_SUCCESS';
export const PUZZLE_GIVEUP = 'PUZZLE_GIVEUP';

export const QUIZ_INIT_DONE = 'QUIZ_INIT_DONE';
export const QUIZ_CHECK_SUCCESS = 'QUIZ_CHECK_SUCCESS';
export const QUIZ_CHECK_FAIL = 'QUIZ_CHECK_FAIL';
export const QUIZ_GIVEUP = 'QUIZ_GIVEUP';
export const QUIZ_NEXT = 'QUIZ_NEXT';
export const QUIZ_PREVIOUS = 'QUIZ_PREVIOUS';


export const prepareInfobox = (json) => {
    if (json.area) {
        json.area = Number(json.area).toLocaleString() + ' ' + localization.km2;
    }
    if (json.population) {
        json.population = Number(json.population).toLocaleString()
    }
    if (json.capital) {
        json.capital.marker = {
            key: json.capital.name,
            defaultAnimation: 2,
            position: {
                lat: json.capital.lat,
                lng: json.capital.lon,
            }
        }
    }
    return json;
};

export const showInfobox = (polygon) => dispatch => {
    if (polygon.infobox.loaded) {
        return dispatch({type: SHOW_INFOBOX, id: polygon.id, data: polygon.infobox});
    } else {
        return fetch(location.origin + `/puzzle/area/` + polygon.id + '/infobox/')
            .then(response => response.json())
            .then(json => dispatch({type: GET_INFOBOX_DONE, id: polygon.id, data: prepareInfobox(json)}))
            .catch(response => dispatch({type: GET_INFOBOX_FAIL}));
    }
};
