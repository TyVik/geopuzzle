'use strict';
import {INIT_PUZZLE_DONE, SHOW_CONGRATULATION} from '../actions';


const infobox = (state = window.__CONGRATULATION__, action) => {
    switch (action.type) {
        case INIT_PUZZLE_DONE:
            return {...state, text: action.countries.map(country => (country.name)).join(', ')};
        case SHOW_CONGRATULATION:
            let time = new Date(Date.now() - state.time);
            let time_result = (time > 24 * 60 * 60 * 1000) ? 'more then day' : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
            let share = state.share + time_result;
            let url = location.href;
            return {...state, show: true, share: share, url: url};
        default:
            return state
    }
};


export default infobox