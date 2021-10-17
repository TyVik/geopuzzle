'use strict';
import React from "react";
import {Button, Modal} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";
import QuizInitForm from "./QuizInitForm";


class QuizInit extends React.Component {
  constructor(props) {
    super(props);
    this.state = props.options.reduce((prev, current) => {prev[current] = true; return prev;}, {});
  }

  toggle = (param) => {
    this.setState(state => ({...state, [param]: !state[param]}));
  };

  renderFooter() {
    if (this.state.name || this.state.flag || this.state.coat_of_arms || this.state.capital) {
      return <Button onClick={() => this.props.load(this.state)}><Msg id="start"/></Button>;
    } else {
      return <React.Fragment>
        <i><Msg id="quizInitCheck"/></i>
        &nbsp;
        <Button disabled={true}><Msg id="start"/></Button>
      </React.Fragment>;
    }
  }

  render() {
    return <Modal show={this.props.show} dialogClassName="custom-modal">
      <Modal.Header>
        <Modal.Title id="contained-modal-title-lg"><Msg id="quizInitCaption"/></Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <QuizInitForm available={this.props.options} data={this.state} toggle={this.toggle}/>
      </Modal.Body>
      <Modal.Footer>
        {this.renderFooter()}
      </Modal.Footer>
    </Modal>;
  }
}


export default QuizInit;
