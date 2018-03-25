'use strict';
import React from "react";
import { connect } from 'react-redux'
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';
import {Button} from "react-bootstrap";

import localization from '../../localization';

import './index.css'
import {PUZZLE_GIVEUP} from "../../actions";


class PuzzleBox extends React.Component {
    giveUp = () => {
        return {ids: this.props.ids, type: PUZZLE_GIVEUP, ws: true};
    };

    render() {
        return (
            <div className="puzzle-box">
                <Toolbox/>
                <Button bsStyle="success" onClick={() => this.props.dispatch(this.giveUp())}>
                    {localization.give_up}
                </Button>
                <div className="infobox-wrapper">
                    <Infobox/>
                </div>
            </div>
        )
    }
};

export default connect(state => {
    return {
        ids: state.polygons.filter(obj => (!obj.isSolved)).map(polygon => (polygon.id))
    }
})(PuzzleBox);
