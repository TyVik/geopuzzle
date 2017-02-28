import {GET_COUNTRIES_DONE, DRAG_END_POLYGON} from '../actions';


const countries = (state = [], action) => {
    switch (action.type) {
        case DRAG_END_POLYGON:
            return state;
        case GET_COUNTRIES_DONE:
            let result = action.countries.map(country => { return {...country, infobox: {}}});
            return result;
        default:
            return state
    }
};


export default countries