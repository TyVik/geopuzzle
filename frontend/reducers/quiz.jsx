'use strict';
import {INIT_QUIZ_DONE} from '../actions';


let init_quiz = {question_ids: window.__IDS__, question: {show: false}};

const infobox = (state = init_quiz, action) => {
    switch (action.type) {
        case INIT_QUIZ_DONE:
            let result = {...state, question_ids: action.countries, answer_ids: [],
                question: action.countries[Math.floor(Math.random() * action.countries.length)]};
            result.question.show = true;
            return result;
        default:
            return state
    }
};


export default infobox