import React from "react";
import {connect} from "react-redux";
import {closeCongratulation} from "../../actions";
import {Modal, Button} from 'react-bootstrap/lib';

// import './index.css'


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
            <Modal show={this.props.show} onHide={this.closeSelf} bsSize="small">
                <Modal.Header closeButton>
                    <Modal.Title>Congratulations!</Modal.Title>
                </Modal.Header>
                <Modal.Body>{this.props.text}</Modal.Body>
                <Modal.Footer>
                    <Button onClick={this.closeSelf}>Close</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}
;


export default connect(state => (state.congratulation))(Congratulation);
