'use strict';
import {PUZZLE_INIT_DONE, QUIZ_INIT_DONE, SHOW_CONGRATULATION} from '../actions';


const infobox = (state = window.__CONGRATULATION__, action) => {
    switch (action.type) {
        case PUZZLE_INIT_DONE:
        case QUIZ_INIT_DONE:
            return {...state, time: Date.now()};
        case SHOW_CONGRATULATION:
            let time = new Date(Date.now() - state.time);
            let time_result = (time > 24 * 60 * 60 * 1000) ? 'more then day' : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
            let url = location.href;
            return {...state, show: true, time_result: time_result, url: url};
        default:
            return state
    }
};


export default infobox;
