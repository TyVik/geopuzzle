'use strict';
import React from "react";
import { connect } from 'react-redux'
import {Button} from "react-bootstrap";

import localization from '../../localization';

import './index.css'
import {PUZZLE_GIVEUP} from "../../actions";


class PuzzleBox extends React.Component {
    render() {
        return (
            <div className="puzzle-box">
                <Button bsStyle="success" onClick={() => this.props.dispatch({type: PUZZLE_GIVEUP})}>
                    {localization.give_up}
                </Button>
            </div>
        )
    }
};

export default connect()(PuzzleBox);
