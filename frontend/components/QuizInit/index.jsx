'use strict';
import React from "react";
import {connect} from "react-redux";
import {Button, Modal, FormGroup, Checkbox} from "react-bootstrap";
import {INIT_QUIZ_DONE, INIT_LOAD_FAIL} from '../../actions';
// import "./index.css";


class QuizInit extends React.Component {
    loadQuiz = this.loadQuiz.bind(this);

    constructor(props) {
        super(props);
        this.state = {show: true, name: false, flag: false, coat_of_arms: false, capital: false};
    }

    loadQuiz() {
        return (dispatch) => {
            this.setState({show: false});
            let quizBy = ['name', 'flag', 'coat_of_arms', 'capital'].filter((param) => this.state[param]);
            let get_params = location.search ? location.search + '&fields=' : '?fields=';
            get_params += quizBy.join();
            return fetch(location.pathname.replace('/quiz/', '/quiz/questions/') + get_params)
                .then(response => response.json())
                .then(questions => dispatch({type: INIT_QUIZ_DONE, questions}))
                .catch(response => dispatch({type: INIT_LOAD_FAIL}));
        };
    }

    toggle(param) {
        this.setState({...this.state, [param]: !this.state[param]});
        console.log(this.state);
    }

    render() {
        return (
            <Modal show={this.state.show} dialogClassName="custom-modal">
                <Modal.Header>
                    <Modal.Title id="contained-modal-title-lg">Choose elements</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <FormGroup>
                        <Checkbox inline onClick={() => this.toggle('name')}>Название</Checkbox>
                        <Checkbox inline onClick={() => this.toggle('flag')}>Флаг</Checkbox>
                        <Checkbox inline onClick={() => this.toggle('coat_of_arms')}>Герб</Checkbox>
                        <Checkbox inline onClick={() => this.toggle('capital')}>Столица</Checkbox>
                    </FormGroup>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={() => this.props.dispatch(this.loadQuiz())}>Start</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}
;

export default connect()(QuizInit);
