'use strict';
import React from "react";
import localization from '../../localization';
import {Button, Modal, FormGroup, Checkbox} from "react-bootstrap";
import "./index.css";


class QuizInit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {show: true, title: false, flag: false, coat_of_arms: false, capital: false};
    }

    toggle(param) {
        this.setState({...this.state, [param]: !this.state[param]});
    }

    allow = () => {
        return this.state.title || this.state.flag || this.state.coat_of_arms || this.state.capital;
    };

    show_checkbox(param) {
        return window.__OPTIONS__.indexOf(param) >= 0;
    }

    render() {
        return (
            <Modal show={this.state.show} dialogClassName="custom-modal">
                <Modal.Header>
                    <Modal.Title id="contained-modal-title-lg">{localization.quizInitCaption}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <FormGroup className="checkbox-group">
                        <Checkbox inline onClick={() => this.toggle('title')}>{localization.title}</Checkbox>
                        {this.show_checkbox('flag') &&
                            <Checkbox inline onClick={() => this.toggle('flag')}>{localization.flag}</Checkbox>
                        }
                        {this.show_checkbox('coat_of_arms') &&
                            <Checkbox inline onClick={() => this.toggle('coat_of_arms')}>{localization.coat_of_arms}</Checkbox>
                        }
                        <Checkbox inline onClick={() => this.toggle('capital')}>{localization.capital}</Checkbox>
                    </FormGroup>
                </Modal.Body>
                <Modal.Footer>
                    {!this.allow() &&
                        <div>
                            {localization.quizInitCheck}&nbsp;
                            <Button disabled>{localization.start}</Button>
                        </div>
                    }
                    {this.allow() &&
                        <Button onClick={() => this.props.load(this.state)}>{localization.start}</Button>
                    }
                </Modal.Footer>
            </Modal>
        );
    }
}


export default QuizInit;
