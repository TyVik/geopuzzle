'use strict';
import React from "react";
import {connect} from "react-redux";
import localization from '../../localization';
import {Button, Modal, FormGroup, Checkbox} from "react-bootstrap";
import {INIT_QUIZ_DONE, INIT_LOAD_FAIL} from "../../actions";
import "./index.css";


class QuizInit extends React.Component {
    loadQuiz = this.loadQuiz.bind(this);
    allow = this.allow.bind(this);

    constructor(props) {
        super(props);
        this.state = {show: true, name: false, flag: false, coat_of_arms: false, capital: false};
    }

    loadQuiz() {
        return (dispatch) => {
            this.setState({show: false});
            let quizBy = ['name', 'flag', 'coat_of_arms', 'capital'].filter((param) => this.state[param]);
            let get_params = location.search ? location.search + '&' : '?';
            get_params += 'params=' + quizBy.join();
            return fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + get_params)
                .then(response => response.json())
                .then(questions => dispatch({type: INIT_QUIZ_DONE, questions}))
                .catch(response => dispatch({type: INIT_LOAD_FAIL}));
        };
    }

    toggle(param) {
        this.setState({...this.state, [param]: !this.state[param]});
    }

    allow() {
        console.log(this.state.name || this.state.flag || this.state.coat_of_arms || this.state.capital);
        return this.state.name || this.state.flag || this.state.coat_of_arms || this.state.capital;
    }

    render() {
        return (
            <Modal show={this.state.show} dialogClassName="custom-modal">
                <Modal.Header>
                    <Modal.Title id="contained-modal-title-lg">{localization.quizInitCaption}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <FormGroup className="checkbox-group">
                        <Checkbox inline onClick={() => this.toggle('name')}>{localization.title}</Checkbox>
                        <Checkbox inline onClick={() => this.toggle('flag')}>{localization.flag}</Checkbox>
                        <Checkbox inline onClick={() => this.toggle('coat_of_arms')}>{localization.coat_of_arms}</Checkbox>
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
                    <Button onClick={() => this.props.dispatch(this.loadQuiz())}>{localization.start}</Button>
                    }
                </Modal.Footer>
            </Modal>
        );
    }
}
;

export default connect()(QuizInit);
