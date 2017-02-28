import {GET_INFOBOX_DONE, CLOSE_INFOBOX} from '../actions';


const infobox = (state = {}, action) => {
    switch (action.type) {
        case CLOSE_INFOBOX:
            return {};
        case GET_INFOBOX_DONE:
            return {...action.data, id: action.id};
        default:
            return state
    }
};


export default infobox