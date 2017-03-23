'use strict';
import {INIT_PUZZLE_DONE, INIT_QUIZ_DONE, SHOW_CONGRATULATION} from '../actions';


const infobox = (state = window.__CONGRATULATION__, action) => {
    switch (action.type) {
        case INIT_PUZZLE_DONE:
        case INIT_QUIZ_DONE:
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


export default infobox