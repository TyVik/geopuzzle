'use strict';
import React from "react";
import {render} from "react-dom";
import {Provider, connect} from "react-redux";
import configureStore from './store';
import Map from './components/Map';
import Loading from './components/Loading';
import Infobox from './components/Infobox';
import QuizQuestion from './components/QuizQuestion';
import QuizInit from './components/QuizInit';
import Toolbox from './components/Toolbox';
import Congratulation from './components/Congratulation';
import {checkQuiz, INIT_LOAD, QUIZ_CHECK} from './actions';


class QuizClass extends React.Component {
    mapInit = this.mapInit.bind(this);
    mapClick = this.mapClick.bind(this);

    mapInit() {
        return {type: INIT_LOAD, url: 'wss://' + window.location.host + '/ws/quiz/'};
    }

    mapClick(e) {
        let question = this.props.questions[this.props.question_index];
        this.props.dispatch({type: QUIZ_CHECK, coords: {lat: e.latLng.lat(), lng: e.latLng.lng()}, id: question.id, ws: true});
    }

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <QuizInit/>
                <QuizQuestion/>
                <Infobox/>
                <Toolbox/>
                <Congratulation/>
            </div>
        )
    };
}

let store = configureStore();
let Quiz = connect(state => (state.quiz))(QuizClass);

render(
    <Provider store={store}>
        <Quiz />
    </Provider>,
    document.getElementById('quiz')
);
