import {GET_COUNTRIES_DONE, CLOSE_CONGRATULATION, SHOW_CONGRATULATION} from '../actions';


const infobox = (state = window.__CONGRATULATION__, action) => {
    switch (action.type) {
        case GET_COUNTRIES_DONE:
            return {...state, text: action.countries.map(country => (country.name)).join(', ')};
        case CLOSE_CONGRATULATION:
            return window.__CONGRATULATION__;
        case SHOW_CONGRATULATION:
            return {...state, show: true};
        default:
            return state
    }
};


export default infobox