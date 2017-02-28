import {GET_INFOBOX_DONE} from '../actions';


const infobox = (state = {}, action) => {
    switch (action.type) {
        case GET_INFOBOX_DONE:
            return {...action.data, id: action.id};
        default:
            return state
    }
};


export default infobox