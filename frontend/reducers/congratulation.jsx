import {GET_COUNTRIES_DONE, CLOSE_CONGRATULATION, SHOW_CONGRATULATION} from '../actions';


let init_congratulation = {show: false};


const infobox = (state = init_congratulation, action) => {
    switch (action.type) {
        case GET_COUNTRIES_DONE:
            return {...state, text: action.countries.map(country => (country.name)).join(', ')};
        case CLOSE_CONGRATULATION:
            return init_congratulation;
        case SHOW_CONGRATULATION:
            return {...state, show: true};
        default:
            return state
    }
};


export default infobox