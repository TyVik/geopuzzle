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
    let questions, question_index;
    switch (action.type) {
        case CHECK_QUIZ_SUCCESS:
            questions = state.questions.filter(element => {return element.id !== action.id});
            question_index = state.question_index % questions.length;
            return {...state, questions: questions, question_index: question_index};
        case INIT_QUIZ_DONE:
            questions = shuffle(action.questions);
            question_index = 0;
            return {...state, questions: questions, question_index: question_index};
        default:
            return state
    }
};


export default quiz