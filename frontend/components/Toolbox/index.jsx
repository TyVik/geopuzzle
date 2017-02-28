import React from "react";
import { connect } from 'react-redux'

import {giveUp} from '../../actions'

import './index.css'


class Toolbox extends React.Component {
    constructor(props) {
        super(props);
        this.reload = this.reload.bind(this);
        this.giveUp = this.giveUp.bind(this);
    }

    reload() {
        location.reload();
    }

    giveUp() {
        this.props.dispatch(giveUp());
    }

    render() {
        return (
            <div className="toolbox_wrapper">
                <div className="btn-group btn-group-sm toolbox">
                    <div className="toolbox_counter">
                        Найдено: <span>{this.props.solved}</span>/<span>{this.props.total}</span>
                    </div>
                    <button type="button" className="btn btn-success" onClick={this.giveUp}>сдаюсь</button>
                    <button type="button" className="btn btn-warning" onClick={this.reload}>ещё раз</button>
                </div>
            </div>
        )
    }
};


export default connect(state => {
    return {
        total: state.map.polygons.length,
        solved: state.map.polygons.filter(obj => (obj.isSolved)).length
    };
})(Toolbox);
