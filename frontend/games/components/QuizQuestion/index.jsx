'use strict';
import React from "react";
import {Button} from "react-bootstrap";
import localization from '../../../localization';

import './index.css'


class QuizQuestion extends React.Component {
  render() {
    if ((this.props.question === null) || (this.props.questions.length === 0)) {
      return null;
    }

    let question = this.props.questions[this.props.question];
    return <div className="quiz-question">
      <table>
        <tbody>
          {question.title && <tr><th className="row_name">{question.title}</th></tr>}
          {question.flag && <tr><td className="row_name"><img src={question.flag}/></td></tr>}
          {question.coat_of_arms && <tr><td className="row_name"><img src={question.coat_of_arms}/></td></tr>}
          {question.capital && <tr><td className="row_name">{question.capital}</td></tr>}
        </tbody>
      </table>
      <div className="quiz-bottom">
        <i className="fas fa-angle-left" onClick={this.props.onPrevious} />
        <Button bsStyle="success" onClick={this.props.giveUp}>
          {localization.give_up}
        </Button>
        <i className="fas fa-angle-right" onClick={this.props.onNext} />
      </div>
    </div>;
  }
}

export default QuizQuestion;
