'use strict';
/* global google */
import React from "react";
import {Collapse} from "react-bootstrap";
import { Scrollbars } from 'react-custom-scrollbars';
import localization from "../../../localization";
import "./index.css";


const NameListItem = (props) => {
  if (!props.polygon.draggable) {
    return <li
        className={"clickable list-group-item list-group-item-" + (props.polygon.isSolved ? 'success' : 'danger')}
        onClick={props.click}>
        {props.polygon.infobox.name}
    </li>;
  } else {
    return <li className="list-group-item list-group-item-danger">&nbsp;</li>;
  }
};


class Toolbox extends React.Component {
  componentWillMount() {
    this.setState({...this.state,
      listNameMaxHeight: window.innerHeight - 220 + "px",
      collapse: JSON.parse(localStorage.getItem('toolbox_collapse')) || false
    });
  }

  toggleCollapse = () => {
    let value = !this.state.collapse;
    localStorage.setItem('toolbox_collapse', value);
    this.setState({collapse: value});
  };

  render() {
    let img = window.__STATIC_URL__;
    let solved = this.props.regions.filter(obj => (obj.isSolved)).length;
    return <div className="toolbox_wrapper">
      <div className="toolbox">
        <div className="listname-wrapper">
          {this.props.wsState !== true &&
            <div id="network_connection_label">{localization.networkError}</div>}
          {localization.found}: <span>{solved}</span>/<span>{this.props.regions.length}</span>
          <span
            className={"glyphicon glyphicon-chevron-" + (this.state.collapse ? 'up' : 'down')}
            onClick={this.toggleCollapse}>
          </span>
{/*
          <Collapse in={!this.state.collapse} onToggle={this.toggleCollapse}>
              <div className="map_switcher_wrapper">
                <img className="map_switcher" src={img + "images/map/terrain.png"}
                     onClick={() => {this.props.setMapType(google.maps.MapTypeId.TERRAIN)}}/>
                <img className="map_switcher" src={img + "images/map/hybrid.png"}
                     onClick={() => {this.props.setMapType(google.maps.MapTypeId.HYBRID)}}/>
                <img className="map_switcher" src={img + "images/map/satellite.png"}
                     onClick={() => {this.props.setMapType(google.maps.MapTypeId.SATELLITE)}}/>
              </div>
                <Scrollbars autoHide={true} autoHeight={true} autoHeightMax={this.state.listNameMaxHeight}>
                  <ul className="list-group">
                    {this.props.regions.map(polygon => (
                      <NameListItem key={polygon.id} polygon={polygon}
                                    click={() => this.props.openInfobox(polygon)}/>
                    ))}
                  </ul>
                </Scrollbars>
          </Collapse>
*/}
        </div>
      </div>
    </div>;
  }
}


export default Toolbox;
