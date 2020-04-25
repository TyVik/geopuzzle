'use strict';
import React from "react";
import {Button, Modal} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";
import QuizInitForm from "./QuizInitForm";


class QuizInit extends React.Component {
  constructor(props) {
    super(props);
    this.state = window.__OPTIONS__.reduce((prev, current) => {prev[current] = true; return prev;}, {});
  }

  toggle = (param) => {
    this.setState({...this.state, [param]: !this.state[param]});
  };

  render_footer() {
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
        <QuizInitForm available={window.__OPTIONS__} data={this.state} toggle={this.toggle}/>
      </Modal.Body>
      <Modal.Footer>
        {this.render_footer()}
      </Modal.Footer>
    </Modal>;
  }
}


export default QuizInit;
