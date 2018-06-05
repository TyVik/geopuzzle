'use strict';
import React from "react";
import QuizInit from '../components/QuizInit/index';
import QuizQuestion from '../components/QuizQuestion/index';
import Game from "./base";
import {decodePolygon, prepareInfobox, shuffle} from "../utils";


class Quiz extends Game {
    GAME_NAME = 'quiz';

    constructor(props) {
        super(props);
        this.state = {...this.state, showInit: true, question: null, questions: []};
    }

    static extractData(polygons, solved) {
        return polygons.map(polygon => {
            return {
                id: polygon.id,
                draggable: true,
                isSolved: false,
                infobox: {name: polygon.name, loaded: false},
                paths: []
            }
        }).concat(solved.map(region => {
            return {
                id: region.id,
                draggable: false,
                isSolved: true,
                infobox: region.infobox,
                paths: decodePolygon(region.polygon)
            }
        })).sort((one, another) => {
            return one.infobox.name > another.infobox.name ? 1 : -1
        });
    }

    dispatchMessage = (event) => {
        let data = JSON.parse(event.data);
        switch(data.type) {
            case 'QUIZ_CHECK_SUCCESS':
            case 'QUIZ_GIVEUP_DONE':
                let regions2 = this.state.regions.map((polygon) => {
                    if (polygon.id === data.id) {
                        return {
                            draggable: false,
                            id: data.id,
                            isSolved: data.type === 'QUIZ_CHECK_SUCCESS',
                            infobox: {...prepareInfobox(data.infobox), loaded: true},
                            paths: decodePolygon(data.polygon)
                        };
                    }
                    return polygon
                });
                let questions = this.state.questions.filter(element => {return element.id !== data.id});
                let index = this.state.question % questions.length;
                this.setState({...this.state, regions: regions2, infobox: data.infobox, questions: questions, question: index});
                break;
        }
    };

    mapClick = (e) => {
        let question = this.state.questions[this.state.question];
        if (question) {
            this.wsSend({type: 'QUIZ_CHECK', coords: {lat: e.latLng.lat(), lng: e.latLng.lng()}, id: question.id});
        }
    };

    loadQuiz = (options) => {
        let quizBy = ['title', 'flag', 'coat_of_arms', 'capital'].filter((param) => options[param]);
        let get_params = location.search ? location.search + '&' : '?';
        get_params += 'params=' + quizBy.join();
        fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + get_params)
            .then(response => response.json())
            .then(data => {
                let regions = Quiz.extractData(data.questions, data.solved);
                this.startGame({regions: regions, questions: shuffle(data.questions), question: 0});
            })
            .catch(response => {this.setState({...this.state, isLoaded: false})});
        this.setState({...this.state, showInit: false});
    };

    giveUp = () => {
        this.wsSend({type: 'QUIZ_GIVEUP', id: this.state.questions[this.state.question].id});
    };

    onNext = () => {
        this.setState({...this.state, question: (this.state.question + 1) % this.state.questions.length});
    };

    onPrevious = () => {
        let index = this.state.question - 1;
        this.setState({...this.state, question: index < 0 ? this.state.questions.length - 1 : index});
    };

    render_question() {
        return <QuizQuestion giveUp={this.giveUp} question={this.state.question} questions={this.state.questions}
                             onNext={this.onNext} onPrevious={this.onPrevious}/>;
    }

    render_popup() {
        return <QuizInit load={this.loadQuiz} show={this.state.showInit}/>;
    }
}


export default Quiz;