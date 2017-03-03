import React from "react";
import {connect} from "react-redux";
import {closeCongratulation} from "../../actions";
import {Modal} from 'react-bootstrap';
import localization from '../../localization';


class Congratulation extends React.Component {
    constructor(props) {
        super(props);
        this.closeSelf = this.closeSelf.bind(this);
    }

    closeSelf() {
        this.props.dispatch(closeCongratulation());
    }

    render() {
        return (
            <Modal show={this.props.show} onHide={this.closeSelf} bsSize="large" aria-labelledby="contained-modal-title-lg">
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-lg">{localization.congratulations}</Modal.Title>
                </Modal.Header>
                <Modal.Body>{this.props.template}: {this.props.text}.</Modal.Body>
            </Modal>
        );
    }
};


export default connect(state => (state.congratulation))(Congratulation);
