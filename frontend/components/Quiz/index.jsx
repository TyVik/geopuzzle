'use strict';
import React from "react";
import { connect } from 'react-redux'

import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import QuizQuestion from '../QuizQuestion';
import Toolbox from '../Toolbox';
import {checkQuiz, INIT_LOAD, INIT_LOAD_FAIL, INIT_QUIZ_DONE} from '../../actions';


class Quiz extends React.Component {
    mapInit = this.mapInit.bind(this);
    mapClick = this.mapClick.bind(this);

    mapInit() {
        return (dispatch) => {
            dispatch({type: INIT_LOAD});
            return fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + location.search)
                .then(response => response.json())
                .then(questions => dispatch({type: INIT_QUIZ_DONE, questions}))
                .catch(response => dispatch({type: INIT_LOAD_FAIL}));
        };
    }

    mapClick(e) {
        return checkQuiz(this.props.id, e.latLng);
    }

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <QuizQuestion/>
                <Infobox/>
                <Toolbox/>
            </div>
        )
    };
}


export default connect(state => (state.quiz.question))(Quiz);
