'use strict';
/* global google */
import React from "react";
import {connect} from "react-redux";
import {Button, Panel} from 'react-bootstrap';
import {giveUp, showCongratulation, setMapType, showInfobox} from "../../actions";
import localization from "../../localization";
import "./index.css";


const NameListItem = (props) => {
    if (!props.polygon.draggable) {
        return (
            <li key={props.polygon.id}
                className={"clickable list-group-item list-group-item-" + (props.polygon.isSolved ? 'success' : 'danger')}
                onClick={props.click}
            >
                {props.polygon.infobox.name}
            </li>
        );
    } else {
        return (
            <li key={props.polygon.id} className="list-group-item list-group-item-danger">---</li>
        );
    }
};


class Toolbox extends React.Component {
    constructor(props) {
        super(props);
        this.reload = this.reload.bind(this);
        this.giveUp = this.giveUp.bind(this);
        this.setMapTerrain = this.setMapTerrain.bind(this);
        this.setMapHybrid = this.setMapHybrid.bind(this);
        this.setMapSatellite = this.setMapSatellite.bind(this);
        this.showInfobox = this.showInfobox.bind(this);
    }

    componentWillMount() {
        this.setState({
            listNameMaxHeight: window.innerHeight - 220 + "px",
            listNameClose: false
        });
    }

    reload() {
        location.reload();
    }

    showInfobox(polygon) {
        this.props.dispatch(showInfobox(polygon));
    }

    giveUp() {
        this.props.dispatch(giveUp());
    }

    setMapTerrain() {
        this.props.dispatch(setMapType(google.maps.MapTypeId.TERRAIN));
    }

    setMapHybrid() {
        this.props.dispatch(setMapType(google.maps.MapTypeId.HYBRID));
    }

    setMapSatellite() {
        this.props.dispatch(setMapType(google.maps.MapTypeId.SATELLITE));
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
                    <div className="map_switcher_wrapper">
                        <img className="map_switcher" src="/static/images/map/terrain.png" onClick={this.setMapTerrain} />
                        <img className="map_switcher" src="/static/images/map/hybrid.png" onClick={this.setMapHybrid} />
                        <img className="map_switcher" src="/static/images/map/satellite.png" onClick={this.setMapSatellite} />
                    </div>
                    <div className="buttons_wrapper">
                        <Button bsStyle="success" onClick={this.giveUp}>{localization.give_up}</Button>
                        <Button bsStyle="warning" onClick={this.reload}>{localization.once_again}</Button>
                    </div>
                    <div className="listname-wrapper">
                        {localization.found}: <span>{this.props.solved}</span>/<span>{this.props.total}</span>
                        <span
                            className={"glyphicon glyphicon-chevron-" + (this.state.listNameClose ? 'up': 'down')}
                            onClick={ ()=> this.setState({ listNameClose: !this.state.listNameClose })}
                        ></span>
                        <Panel collapsible expanded={!this.state.listNameClose}>
                            <ul className="list-group" style={{maxHeight: this.state.listNameMaxHeight}}>
                                {this.props.countries.map(polygon => (
                                    <NameListItem key={polygon.id} polygon={polygon} click={() => this.showInfobox(polygon)}/>
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
