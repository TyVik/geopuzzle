'use strict';
import React from "react";
import { connect } from 'react-redux'

import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import QuizQuestion from '../QuizQuestion';
import Toolbox from '../Toolbox';
import {initQuiz, checkQuiz} from '../../actions';


class Quiz extends React.Component {
    mapInit = this.mapInit.bind(this);
    mapClick = this.mapClick.bind(this);

    mapInit() {
        return initQuiz();
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
