'use strict';
import React from "react";
import { connect } from 'react-redux'
import {Button} from "react-bootstrap";

import localization from '../../localization';
import {QUIZ_GIVEUP, QUIZ_NEXT, QUIZ_PREVIOUS} from "../../actions";

import './index.css'


class QuizQuestion extends React.Component {
    render() {
        if (this.props.questions && (this.props.questions.length > 0)) {
            let question = this.props.questions[this.props.question_index];
            console.log(question);
            return (
                <div className="quiz-question">
                    <table>
                        <tbody>
                        <tr>
                            <th colSpan="2" className="row_name">
                                {question.name}
                            </th>
                        </tr>
                        {question.image &&
                            <tr>
                                <td colSpan="2">
                                    <img src={question.image}/>
                                </td>
                            </tr>
                        }
                        {question.capital &&
                            <tr>
                                <td>{localization['capital']}</td>
                                <td>{question.capital}</td>
                            </tr>
                        }
                        </tbody>
                    </table>
                    <div className="quiz-bottom">
                        <span
                            className="glyphicon glyphicon-chevron-left"
                            onClick={() => this.props.dispatch({type: QUIZ_PREVIOUS})}>
                        </span>
                        <Button bsStyle="success" onClick={() => this.props.dispatch({type: QUIZ_GIVEUP, id: this.props.id})}>
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
