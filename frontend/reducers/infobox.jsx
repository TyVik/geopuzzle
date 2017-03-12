'use strict';
import {GET_INFOBOX_DONE, CLOSE_INFOBOX, GIVE_UP, SHOW_INFOBOX} from '../actions';


let init_infobox = {show: false};

const infobox = (state = init_infobox, action) => {
    switch (action.type) {
        case GIVE_UP:
            return init_infobox;
        case CLOSE_INFOBOX:
            return init_infobox;
        case SHOW_INFOBOX:
            return {...action.data, show: true};
        case GET_INFOBOX_DONE:
            return {...action.data, show: true};
        default:
            return state
    }
};


export default infobox