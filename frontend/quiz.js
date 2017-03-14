'use strict';
import React from "react";
import {render} from "react-dom";
import {Provider, connect} from "react-redux";
import configureStore from './store';
import Map from './components/Map';
import Loading from './components/Loading';
import Infobox from './components/Infobox';
import QuizQuestion from './components/QuizQuestion';
import Toolbox from './components/Toolbox';
import {checkQuiz, INIT_LOAD, INIT_LOAD_FAIL, INIT_QUIZ_DONE, CHECK_QUIZ_FAIL, CHECK_QUIZ_SUCCESS} from './actions';


class QuizClass extends React.Component {
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
        return (dispatch) => {
            let formData = new FormData();
            formData.append('lat', e.latLng.lat());
            formData.append('lng', e.latLng.lng());
            let options = {
                method: 'POST',
                body: formData
            };
            return fetch('//' + location.host + '/quiz/' + this.props.id + '/check/', options)
                .then(response => response.json())
                .then(json => {
                    if (json.success) {
                        return dispatch({...json, type: CHECK_QUIZ_SUCCESS, id: this.props.id})
                    } else {
                        return dispatch({type: CHECK_QUIZ_FAIL});
                    }
                })
                .catch(response => {
                    return dispatch({type: CHECK_QUIZ_FAIL});
                });
        };
    }

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <QuizQuestion/>
                <Infobox/>
                <Toolbox showButtons={false}/>
            </div>
        )
    };
}

let store = configureStore();
let Quiz = connect(state => (state.quiz.question))(QuizClass);

render(
    <Provider store={store}>
        <Quiz />
    </Provider>,
    document.getElementById('quiz')
);
