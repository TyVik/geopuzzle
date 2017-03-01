export const GET_COUNTRIES = 'GET_COUNTRIES';
export const GET_COUNTRIES_FAIL = 'GET_COUNTRIES_FAIL';
export const GET_COUNTRIES_DONE = 'GET_COUNTRIES_DONE';
export const DRAG_END_POLYGON = 'DRAG_END_POLYGON';
export const DRAG_END_POLYGON_FAIL = 'DRAG_END_POLYGON_FAIL';
export const GET_INFOBOX_DONE = 'GET_INFOBOX_DONE';
export const GET_INFOBOX_FAIL = 'GET_INFOBOX_FAIL';
export const CLOSE_INFOBOX = 'CLOSE_INFOBOX';
export const SHOW_INFOBOX = 'SHOW_INFOBOX';
export const SHOW_INFOBOX_BY_ID = 'SHOW_INFOBOX_BY_ID';
export const GIVE_UP = 'GIVE_UP';


export const sendRequest = () => ({
  type: GET_COUNTRIES,
});


export const updateCountries = (success, countries) => {
    if (success === false) {
        return {type: GET_COUNTRIES_FAIL};
    } else {
        return {type: GET_COUNTRIES_DONE, countries}
    }
};


export const getCountries = () => dispatch => {
    dispatch(sendRequest());
    return fetch(`http://127.0.0.1:8000/maps/questions/italy?id=15&id=16`)
        .then(response => response.json())
        .then(json => dispatch(updateCountries(true, json)))
        .catch(response => dispatch(updateCountries(false)));
};


export const updateInfobox = (success, id, json) => {
    if (success === false) {
        return {type: GET_INFOBOX_FAIL};
    } else {
        return {type: GET_INFOBOX_DONE, id: id, data: json}
    }
};


export const showInfoboxById = (id, data) => {
    return {type: SHOW_INFOBOX_BY_ID, id: id, data: data};
};


export const showInfobox = (polygonId) => dispatch => {
    return fetch(`http://127.0.0.1:8000/maps/area/` + polygonId + '/infobox/')
        .then(response => response.json())
        .then(json => dispatch(updateInfobox(true, polygonId, json)))
        .catch(response => dispatch(updateInfobox(false)));
};


export const closeInfobox = () => ({
    type: CLOSE_INFOBOX,
});


export const giveUp = () => ({
    type: GIVE_UP,
});