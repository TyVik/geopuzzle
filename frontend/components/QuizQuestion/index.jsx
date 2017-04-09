'use strict';
import React from "react";
import { connect } from 'react-redux'
import {Button} from "react-bootstrap";

import localization from '../../localization';
import {QUIZ_GIVEUP, QUIZ_NEXT, QUIZ_PREVIOUS, INIT_LOAD_FAIL} from "../../actions";

import './index.css'


class QuizQuestion extends React.Component {
    giveUp = this.giveUp.bind(this);

    giveUp() {
        let question = this.props.questions[this.props.question_index];
        this.props.dispatch({type: QUIZ_GIVEUP, id: question.id, ws: true});
    }

    render() {
        if (this.props.questions && (this.props.questions.length > 0)) {
            let question = this.props.questions[this.props.question_index];
            return (
                <div className="quiz-question">
                    <table>
                        <tbody>
                        {question.name &&
                            <tr><th className="row_name">{question.name}</th></tr>
                        }
                        {question.flag &&
                            <tr><td className="row_name"><img src={question.flag}/></td></tr>
                        }
                        {question.coat_of_arms &&
                            <tr><td className="row_name"><img src={question.coat_of_arms}/></td></tr>
                        }
                        {question.capital &&
                            <tr><td className="row_name">{question.capital}</td></tr>
                        }
                        </tbody>
                    </table>
                    <div className="quiz-bottom">
                        <span
                            className="glyphicon glyphicon-chevron-left"
                            onClick={() => this.props.dispatch({type: QUIZ_PREVIOUS})}>
                        </span>
                        <Button bsStyle="success" onClick={this.giveUp}>
                            {localization.give_up}
                        </Button>
                        <span
                            className="glyphicon glyphicon-chevron-right"
                            onClick={() => this.props.dispatch({type: QUIZ_NEXT})}>
                        </span>
                    </div>
                </div>
            )
        } else {
            return null;
        }
    }
};

export default connect(state => (state.quiz))(QuizQuestion);
