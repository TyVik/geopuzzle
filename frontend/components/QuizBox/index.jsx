'use strict';
import React from "react";
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';
import QuizQuestion from '../QuizQuestion';

import './index.css'


class QuizBox extends React.Component {
    render() {
        return (
            <div className="quiz-box">
                <Toolbox/>
                <QuizQuestion/>
                <div className="infobox-wrapper">
                    <Infobox/>
                </div>
            </div>
        )
    }
}

export default QuizBox;
