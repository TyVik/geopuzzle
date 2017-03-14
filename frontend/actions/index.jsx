'use strict';
import "whatwg-fetch";
import localization from "../localization";

export const INIT_QUIZ_FAIL = 'INIT_QUIZ_FAIL';
export const INIT_QUIZ_DONE = 'INIT_QUIZ_DONE';
export const CHECK_QUIZ_SUCCESS = 'CHECK_QUIZ_SUCCESS';
export const CHECK_QUIZ_FAIL = 'CHECK_QUIZ_FAIL';
export const GET_COUNTRIES = 'GET_COUNTRIES';
export const GET_COUNTRIES_FAIL = 'GET_COUNTRIES_FAIL';
export const GET_COUNTRIES_DONE = 'GET_COUNTRIES_DONE';
export const DRAG_END_POLYGON = 'DRAG_END_POLYGON';
export const DRAG_END_POLYGON_FAIL = 'DRAG_END_POLYGON_FAIL';
export const GET_INFOBOX_DONE = 'GET_INFOBOX_DONE';
export const GET_INFOBOX_FAIL = 'GET_INFOBOX_FAIL';
export const SHOW_INFOBOX = 'SHOW_INFOBOX';
export const GIVE_UP = 'GIVE_UP';
export const SET_MAP_TYPE = 'SET_MAP_TYPE';
export const SHOW_CONGRATULATION = 'SHOW_CONGRATULATION';
export const CLOSE_CONGRATULATION = 'CLOSE_CONGRATULATION';


export const sendRequest = () => ({type: GET_COUNTRIES});

export const checkQuiz = (id, latLng) => dispatch => {
    let formData = new FormData();
    formData.append('lat', latLng.lat());
    formData.append('lng', latLng.lng());
    let options = {
        method: 'POST',
        body: formData
    };
    return fetch('//' + location.host + '/quiz/' + id + '/check/', options)
        .then(response => response.json())
        .then(json => {
            if (json.success) {
                return dispatch({...json, type: CHECK_QUIZ_SUCCESS, id: id})
            } else {
                return dispatch({type: CHECK_QUIZ_FAIL});
            }
        })
        .catch(response => {
            return dispatch({type: CHECK_QUIZ_FAIL});
        });
};

export const initQuiz = () => dispatch => {
    dispatch(sendRequest());
    return fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + location.search)
        .then(response => response.json())
        .then(questions => dispatch({type: INIT_QUIZ_DONE, questions}))
        .catch(response => dispatch({type: INIT_QUIZ_FAIL}));
};

export const getCountries = () => dispatch => {
    dispatch(sendRequest());
    return fetch(location.pathname.replace('/maps/', '/maps/questions/') + location.search)
        .then(response => response.json())
        .then(countries => dispatch({type: GET_COUNTRIES_DONE, countries}))
        .catch(response => dispatch({type: GET_COUNTRIES_FAIL}));
};

export const updateInfobox = (success, id, json) => {
    if (success === false) {
        return {type: GET_INFOBOX_FAIL};
    } else {
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
        return {type: GET_INFOBOX_DONE, id: id, data: json}
    }
};
export const showInfobox = (polygon) => dispatch => {
    if (polygon.infobox.loaded) {
        return dispatch({type: SHOW_INFOBOX, id: polygon.id, data: polygon.infobox});
    } else {
        return fetch(location.origin + `/maps/area/` + polygon.id + '/infobox/')
            .then(response => response.json())
            .then(json => dispatch(updateInfobox(true, polygon.id, json)))
            .catch(response => dispatch(updateInfobox(false)));
    }
};

export const giveUp = () => ({type: GIVE_UP});

export const showCongratulation = () => ({type: SHOW_CONGRATULATION});
export const closeCongratulation = () => ({type: CLOSE_CONGRATULATION});

export const setMapType = (mapType) => ({type: SET_MAP_TYPE, value: mapType});
