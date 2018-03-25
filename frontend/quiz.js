'use strict';
import React from "react";
import {render} from "react-dom";
import {Provider, connect} from "react-redux";
import configureStore from './store';
import Map from './components/Map';
import QuizBox from './components/QuizBox';
import QuizInit from './components/QuizInit';
import {checkQuiz, INIT_LOAD, QUIZ_CHECK, QUIZ_INIT_DONE} from './actions';
import Game from "./components/Game";


class QuizClass extends Game {
    constructor(props) {
        super(props);
        this.state = {isLoaded: null, showInit: true, congratulation: {show: false, startTime: null}};
    }

    mapInit = () => {
        return {type: INIT_LOAD, game: 'quiz'};
    };

    mapClick = (e) => {
        let question = this.props.questions[this.props.question_index];
        this.props.dispatch({type: QUIZ_CHECK, coords: {lat: e.latLng.lat(), lng: e.latLng.lng()}, id: question.id, ws: true});
    };

    loadQuiz = (options) => {
        return (dispatch) => {
            this.setState({...this.state, showInit: false});
            let quizBy = ['title', 'flag', 'coat_of_arms', 'capital'].filter((param) => options[param]);
            let get_params = location.search ? location.search + '&' : '?';
            get_params += 'params=' + quizBy.join();
            return fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + get_params)
                .then(response => response.json())
                .then(questions => {
                    dispatch({type: QUIZ_INIT_DONE, ...questions});
                    this.startGame();
                })
                .catch(response => {this.setState({...this.state, isLoaded: false})});
        };
    };

    render() {
        return (
            <div>
                {this.render_loaded()}
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                {this.state.showInit &&
                    <QuizInit load={this.loadQuiz} />}
                <QuizBox showCongrats={this.showCongratulation}/>
                {this.render_congratulation()}
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
