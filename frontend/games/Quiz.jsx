'use strict';
import React from "react";
import {QuizInit} from './components/QuizInit/index';
import QuizQuestion from './components/QuizQuestion/index';
import Game from "./Game";
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

  static prepareQuestions(questions) {
    return shuffle(questions
      .map(question => {
        return ['name', 'flag', 'coat_of_arms', 'capital']
          .map(key => {
            if (question[key] === undefined) {
              return null;
            }
            let result = {id: question.id};
            result[key] = question[key];
            return result;
          })
          .filter(item => item !== null);
    }).reduce((l, acc) => {acc = acc.concat(l); return acc}, []));
  }

  changeRegionState(data, current) {
    let regions = this.state.regions.map((polygon) => {
      if (polygon.id === data.id) {
        return {
          draggable: false,
          id: data.id,
          isSolved: data.type === 'QUIZ_CHECK_SUCCESS',
          infobox: {...prepareInfobox(data.infobox), loaded: true},
          paths: decodePolygon(data.polygon),
        };
      }
      return polygon;
    });
    let questions = this.state.questions.filter(element => {return element.id !== data.id});
    let index = current === null ? this.state.question % questions.length : questions.findIndex(item => item.id === current.id);
    if (index === -1) {
      index = this.state.question % questions.length;
    }
    let infobox = current === null ? {...data.infobox} : this.state.infobox;
    this.setState({...this.state, regions: regions, infobox: infobox, questions: questions, question: index});
  }

  dispatchMessage = (event) => {
    let data = JSON.parse(event.data);
    switch(data.type) {
      case 'QUIZ_CHECK_SUCCESS':
      case 'QUIZ_GIVEUP_DONE':
        this.changeRegionState(data, null);
        break;
      case 'QUIZ_FOUND':
        this.changeRegionState(data, this.state.questions[this.state.question]);
        break;
      default:
        this._dispatchMessage(event);
    }
  };

  mapClick = (e) => {
    let question = this.state.questions[this.state.question];
    if (question) {
      this.wsSend({type: 'QUIZ_CHECK', coords: {lat: e.latLng.lat(), lng: e.latLng.lng()}, id: question.id});
    }
  };

  loadQuiz = (options) => {
    let quizBy = ['name', 'flag', 'coat_of_arms', 'capital'].filter((param) => options[param]);
    let get_params = location.search ? location.search + '&' : '?';
    get_params += 'params=' + quizBy.join();
    fetch(`${location.pathname}questions/${get_params}`)
      .then(response => response.json())
      .then(data => {
        let regions = Quiz.extractData(data.questions, data.solved);
        this.startGame({regions: regions, questions: Quiz.prepareQuestions(data.questions), question: 0});
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
