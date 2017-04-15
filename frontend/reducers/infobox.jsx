'use strict';
import {GET_INFOBOX_DONE, SHOW_INFOBOX, CLOSE_INFOBOX, QUIZ_CHECK_SUCCESS, QUIZ_GIVEUP, PUZZLE_CHECK_SUCCESS,
e3wprepareInfobox} from '../actions';


let init_infobox = {show: false};

const infobox = (state = init_infobox, action) => {
    switch (action.type) {
        case QUIZ_CHECK_SUCCESS:
        case PUZZLE_CHECK_SUCCESS:
        case QUIZ_GIVEUP:
            let json = prepareInfobox(action.infobox);
            return {...json, show: true};
        case SHOW_INFOBOX:
        case GET_INFOBOX_DONE:
            let data = prepareInfobox(action.data);
            return {...data, show: true};
        case CLOSE_INFOBOX:
            return init_infobox;
        default:
            return state
    }
};


export default infobox