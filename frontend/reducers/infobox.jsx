'use strict';
import {GET_INFOBOX_DONE, SHOW_INFOBOX, CLOSE_INFOBOX, CHECK_QUIZ_SUCCESS, QUIZ_GIVEUP, PUZZLE_CHECK_SUCCESS} from '../actions';


let init_infobox = {show: false};

const infobox = (state = init_infobox, action) => {
    switch (action.type) {
        case CHECK_QUIZ_SUCCESS:
        case PUZZLE_CHECK_SUCCESS:
        case QUIZ_GIVEUP:
            return {...action.infobox, show: true};
        case SHOW_INFOBOX:
            return {...action.data, show: true};
        case GET_INFOBOX_DONE:
            return {...action.data, show: true};
        case CLOSE_INFOBOX:
            return init_infobox;
        default:
            return state
    }
};


export default infobox