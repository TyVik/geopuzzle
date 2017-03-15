'use strict';
/* global google */
import React from "react";
import {connect} from "react-redux";
import {Panel} from "react-bootstrap";
import {SHOW_CONGRATULATION, SET_MAP_TYPE, showInfobox} from "../../actions";
import localization from "../../localization";
import "./index.css";


const NameListItem = (props) => {
    if (!props.polygon.draggable) {
        return (
            <li key={props.polygon.id}
                className={"clickable list-group-item list-group-item-" + (props.polygon.isSolved ? 'success' : 'danger')}
                onClick={props.click}>
                {props.polygon.infobox.name}
            </li>
        );
    } else {
        return (
            <li key={props.polygon.id} className="list-group-item list-group-item-danger">&nbsp;</li>
        );
    }
};


class Toolbox extends React.Component {
    componentWillMount() {
        this.setState({...this.state,
            listNameMaxHeight: window.innerHeight - 220 + "px",
            listNameClose: false
        });
    }

    componentWillReceiveProps(props) {
        if (props.total === props.solved) {
            this.props.dispatch({type: SHOW_CONGRATULATION});
        }
    }

    render() {
        return (
            <div className="toolbox_wrapper">
                <div className="btn-group btn-group-sm toolbox">
                    <div className="map_switcher_wrapper">
                        <img className="map_switcher" src="/static/images/map/terrain.png"
                             onClick={() => this.props.dispatch({
                                 type: SET_MAP_TYPE,
                                 value: google.maps.MapTypeId.TERRAIN
                             })}/>
                        <img className="map_switcher" src="/static/images/map/hybrid.png"
                             onClick={() => this.props.dispatch({
                                 type: SET_MAP_TYPE,
                                 value: google.maps.MapTypeId.HYBRID
                             })}/>
                        <img className="map_switcher" src="/static/images/map/satellite.png"
                             onClick={() => this.props.dispatch({
                                 type: SET_MAP_TYPE,
                                 value: google.maps.MapTypeId.SATELLITE
                             })}/>
                    </div>
                    <div className="listname-wrapper">
                        {localization.found}: <span>{this.props.solved}</span>/<span>{this.props.total}</span>
                        <span
                            className={"glyphicon glyphicon-chevron-" + (this.state.listNameClose ? 'up' : 'down')}
                            onClick={() => this.setState({listNameClose: !this.state.listNameClose})}>
                        </span>
                        <Panel collapsible expanded={!this.state.listNameClose}>
                            <ul className="list-group" style={{maxHeight: this.state.listNameMaxHeight}}>
                                {this.props.countries.map(polygon => (
                                    <NameListItem key={polygon.id} polygon={polygon}
                                                  click={() => this.props.dispatch(showInfobox(polygon))}/>
                                ))}
                            </ul>
                        </Panel>
                    </div>
                </div>
            </div>
        )
    }
}
;


export default connect(state => {
    return {
        total: state.polygons.length,
        solved: state.polygons.filter(obj => (obj.isSolved)).length,
        countries: state.polygons
    };
})(Toolbox);
