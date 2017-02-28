import {GET_COUNTRIES_DONE} from '../actions';


const countries = (state = [], action) => {
    switch (action.type) {
        case GET_COUNTRIES_DONE:
            return action.countries.map(country => { return {...country, infobox: {}}});
        default:
            return state
    }
};


export default countries