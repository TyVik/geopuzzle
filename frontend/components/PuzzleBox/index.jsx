'use strict';
import React from "react";
import { connect } from 'react-redux'
import {Button} from "react-bootstrap";

import localization from '../../localization';

import './index.css'
import {GIVE_UP} from "../../actions";


class PuzzleBox extends React.Component {
    render() {
        return (
            <div className="puzzle-box">
                <Button bsStyle="success" onClick={() => this.props.dispatch({type: GIVE_UP})}>
                    {localization.give_up}
                </Button>
            </div>
        )
    }
};

export default connect()(PuzzleBox);
