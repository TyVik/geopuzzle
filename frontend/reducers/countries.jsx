import {GET_COUNTRIES_DONE, GET_INFOBOX_DONE} from '../actions';


const countries = (state = [], action) => {
    switch (action.type) {
        case GET_INFOBOX_DONE:
            return state.map((country) => {
                if (country.id === action.id) {
                    return {...country, infobox: action.data};
                }
                return country
            });
        case GET_COUNTRIES_DONE:
            return action.countries.map(country => { return {...country, infobox: {}}});
        default:
            return state
    }
};


export default countries