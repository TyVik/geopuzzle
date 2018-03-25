'use strict';
import {GET_INFOBOX_DONE, SHOW_INFOBOX, CLOSE_INFOBOX, QUIZ_CHECK_SUCCESS, QUIZ_GIVEUP_DONE, PUZZLE_CHECK_SUCCESS} from '../actions';


let init_infobox = {show: false};

const infobox = (state = init_infobox, action) => {
    switch (action.type) {
        case QUIZ_CHECK_SUCCESS:
        case QUIZ_GIVEUP_DONE:
        case PUZZLE_CHECK_SUCCESS:
        case GET_INFOBOX_DONE:
        case SHOW_INFOBOX:
            return {...action.infobox, show: true};
        case CLOSE_INFOBOX:
            return init_infobox;
        default:
            return state
    }
};


export default infobox;
