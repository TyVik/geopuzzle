'use strict';
import {INIT_QUIZ_DONE, CHECK_QUIZ_SUCCESS} from '../actions';


let init_quiz = {question: {show: false}};

function shuffle(a) {
    for (let i = a.length; i; i--) {
        let j = Math.floor(Math.random() * i);
        [a[i - 1], a[j]] = [a[j], a[i - 1]];
    }
    return a;
}

const quiz = (state = init_quiz, action) => {
    let questions, question;
    switch (action.type) {
        case CHECK_QUIZ_SUCCESS:
            questions = state.questions;
            question = questions.shift();
            return {...state, question: {...question, show: question !== undefined}, questions: questions};
        case INIT_QUIZ_DONE:
            questions = shuffle(action.questions);
            question = questions.shift();
            return {...state, questions: questions, question: {...question, show: true}};
        default:
            return state
    }
};


export default quiz