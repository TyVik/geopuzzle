'use strict';
import React from "react";
import localization from '../../../localization';
import {Button, Modal, FormGroup, Checkbox} from "react-bootstrap";
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
      return <Button onClick={() => this.props.load(this.state)}>{localization.start}</Button>;
    } else {
      return <React.Fragment>
        <i>{localization.quizInitCheck}</i>
        &nbsp;
        <Button disabled>{localization.start}</Button>
      </React.Fragment>;
    }
  }

  render() {
    return <Modal show={this.props.show} dialogClassName="custom-modal">
      <Modal.Header>
        <Modal.Title id="contained-modal-title-lg">{localization.quizInitCaption}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <FormGroup className="checkbox-group">
          <Checkbox inline onClick={() => this.toggle('title')} defaultChecked={this.state['title']}>{localization.title}</Checkbox>
          {QuizInit.show_checkbox('flag') &&
            <Checkbox inline onClick={() => this.toggle('flag')} defaultChecked={this.state['flag']}>{localization.flag}</Checkbox>}
          {QuizInit.show_checkbox('coat_of_arms') &&
            <Checkbox inline onClick={() => this.toggle('coat_of_arms')} defaultChecked={this.state['coat_of_arms']}>{localization.coat_of_arms}</Checkbox>}
            <Checkbox inline onClick={() => this.toggle('capital')} defaultChecked={this.state['capital']}>{localization.capital}</Checkbox>
        </FormGroup>
      </Modal.Body>
      <Modal.Footer>
        {this.render_footer()}
      </Modal.Footer>
    </Modal>;
  }
}


export default QuizInit;
