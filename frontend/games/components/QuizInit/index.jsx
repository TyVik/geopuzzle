'use strict';
import React from "react";
import {Button, Modal, FormGroup, Form} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";


class QuizInit extends React.Component {
  constructor(props) {
    super(props);
    this.state = {title: true, flag: true, coat_of_arms: true, capital: true};
  }

  toggle(param) {
    this.setState({...this.state, [param]: !this.state[param]});
  }

  static show_checkbox(param) {
    return window.__OPTIONS__.indexOf(param) >= 0;
  }

  render_footer() {
    if (this.state.title || this.state.flag || this.state.coat_of_arms || this.state.capital) {
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
        <FormGroup className="checkbox-group" controlId="quiz">
          <Form.Check inline label={<Msg id="title"/>} onClick={() => this.toggle('title')} type="checkbox" defaultChecked={this.state['title']}/>
          {QuizInit.show_checkbox('flag') &&
            <Form.Check inline label={<Msg id="flag"/>} onClick={() => this.toggle('flag')} type="checkbox" defaultChecked={this.state['flag']} />}
          {QuizInit.show_checkbox('coat_of_arms') &&
            <Form.Check inline label={<Msg id="coat_of_arms"/>} onClick={() => this.toggle('coat_of_arms')} type="checkbox" defaultChecked={this.state['coat_of_arms']}/>}
            <Form.Check inline label={<Msg id="capital"/>} onClick={() => this.toggle('capital')} type="checkbox" defaultChecked={this.state['capital']} />
        </FormGroup>
      </Modal.Body>
      <Modal.Footer>
        {this.render_footer()}
      </Modal.Footer>
    </Modal>;
  }
}


export default QuizInit;
