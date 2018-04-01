'use strict';
import React from "react";
import {render} from "react-dom";
import Sockette from 'sockette';
import Map from '../Map';
import QuizInit from '../QuizInit';
import QuizQuestion from '../QuizQuestion';
import {QUIZ_CHECK, QUIZ_CHECK_SUCCESS, QUIZ_GIVEUP, QUIZ_GIVEUP_DONE} from '../../actions';
import Game from "../Game";
import {decodePolygon, prepareInfobox, shuffle} from "../../utils";
import Toolbox from "../Toolbox";
import Infobox from "../Infobox";


import './index.css';


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
            case QUIZ_CHECK_SUCCESS:
            case QUIZ_GIVEUP_DONE:
                let regions2 = this.state.regions.map((polygon) => {
                    if (polygon.id === data.id) {
                        return {
                            draggable: false,
                            id: data.id,
                            isSolved: data.type === QUIZ_CHECK_SUCCESS,
                            infobox: {...prepareInfobox(data.infobox), loaded: true},
                            paths: decodePolygon(data.polygon)
                        };
                    }
                    return polygon
                });
                let questions = this.state.questions.filter(element => {return element.id !== data.id});
                let index = this.state.question % this.state.questions.length;
                this.setState({...this.state, regions: regions2, infobox: data.infobox, questions: questions, question: index});
                break;
        }
    };

    mapClick = (e) => {
        let question = this.state.questions[this.state.question];
        this.ws.json({type: QUIZ_CHECK, coords: {lat: e.latLng.lat(), lng: e.latLng.lng()}, id: question.id});
    };

    loadQuiz = (options) => {
        let quizBy = ['title', 'flag', 'coat_of_arms', 'capital'].filter((param) => options[param]);
        let get_params = location.search ? location.search + '&' : '?';
        get_params += 'params=' + quizBy.join();
        fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + get_params)
            .then(response => response.json())
            .then(data => {
                let regions = Quiz.extractData(data.questions, data.solved);
                let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
                let addr = ws_scheme + '://' + window.location.host + '/ws/' + this.GAME_NAME + '/';
                this.ws = new Sockette(addr, {
                    timeout: 5e3,
                    maxAttempts: 10,
                    onopen: e => this.setState({...this.state, wsState: true}),
                    onmessage: e => this.dispatchMessage(e),
                    onreconnect: e => this.setState({...this.state, wsState: null}),
                    onmaximum: e => this.setState({...this.state, wsState: false}),
                    onclose: e => this.setState({...this.state, wsState: null}),
                    onerror: e => this.setState({...this.state, wsState: false})
                });
                this.startGame({regions: regions, questions: shuffle(data.questions), question: 0});
            })
            .catch(response => {this.setState({...this.state, isLoaded: false})});
        this.setState({...this.state, showInit: false});
    };

    giveUp = () => {
        this.ws.json({type: QUIZ_GIVEUP, id: this.state.questions[this.state.question].id});
    };

    onNext = () => {
        this.setState({...this.state, question: (this.state.question + 1) % this.state.questions.length});
    };

    onPrevious = () => {
        let index = this.state.question - 1;
        this.setState({...this.state, question: index < 0 ? this.state.questions.length - 1 : index});
    };

    render() {
        return (
            <div>
                {this.render_loaded()}
                <Map mapClick={this.mapClick} mapTypeId={this.state.map.typeId}
                     regions={this.state.regions} onPolygonClick={this.onPolygonClick}/>
                <QuizInit load={this.loadQuiz} show={this.state.showInit}/>
                <div className="quiz-box">
                    <Toolbox setMapType={this.setMapType} regions={this.state.regions} wsState={this.state.wsState}
                             showInfobox={this.showInfobox}/>
                    {<QuizQuestion giveUp={this.giveUp} question={this.state.question}
                                   questions={this.state.questions} onNext={this.onNext} onPrevious={this.onPrevious}/>}
                    <div className="infobox-wrapper">
                        <Infobox {...this.state.infobox} show={true}/>
                    </div>
                </div>
                {this.render_congratulation()}
            </div>
        )
    };
}


export default Quiz;