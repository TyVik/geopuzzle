import React from "react";
import {connect} from "react-redux";
import {giveUp, showCongratulation} from "../../actions";
import localization from "../../localization";
import "./index.css";


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

    componentWillReceiveProps(props) {
        if (props.total === props.solved) {
            this.props.dispatch(showCongratulation());
        }
    }

    render() {
        return (
            <div className="toolbox_wrapper">
                <div className="btn-group btn-group-sm toolbox">
                    <div className="toolbox_counter">
                        {localization.found}: <span>{this.props.solved}</span>/<span>{this.props.total}</span>
                    </div>
                    <button type="button" className="btn btn-success" onClick={this.giveUp}>{localization.give_up}</button>
                    <button type="button" className="btn btn-warning" onClick={this.reload}>{localization.once_again}</button>
                </div>
            </div>
        )
    }
}
;


export default connect(state => {
    return {
        total: state.polygons.length,
        solved: state.polygons.filter(obj => (obj.isSolved)).length
    };
})(Toolbox);
