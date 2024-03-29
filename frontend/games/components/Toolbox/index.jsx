'use strict';
/* global google */
import React from "react";
import {Collapse} from "react-bootstrap";
import { Scrollbars } from 'react-custom-scrollbars';
import ListGroup from "react-bootstrap/ListGroup";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";


const NameListItem = (props) => {
  if (props.polygon.isOpen) {
    return <ListGroup.Item variant={props.polygon.isSolved ? 'success' : 'danger'} onClick={props.click} action={true}>
      {props.polygon.infobox.name}
    </ListGroup.Item>;
  } else {
    return <ListGroup.Item variant="danger">&nbsp;</ListGroup.Item>;
  }
};


class Toolbox extends React.Component {
  COLLAPSE_ID = 'toolbox-collapse';

  constructor(props) {
    super(props);
    this.state = {
      listNameMaxHeight: window.innerHeight - 220 + "px",
      collapse: JSON.parse(localStorage.getItem('toolbox-collapse')) || false,
    };
  }

  toggleCollapse = () => {
    let value = !this.state.collapse;
    localStorage.setItem('toolbox-collapse', value);
    this.setState({collapse: value});
  };


  switchMap() {
    let img = window.__STATIC_URL__;

    return <div className="map-switcher-wrapper">
      <img className="map-switcher" src={img + "images/map/terrain.png"}
           onClick={() => {this.props.setMapType(google.maps.MapTypeId.TERRAIN)}}/>
      <img className="map-switcher" src={img + "images/map/hybrid.png"}
           onClick={() => {this.props.setMapType(google.maps.MapTypeId.HYBRID)}}/>
      <img className="map-switcher" src={img + "images/map/satellite.png"}
           onClick={() => {this.props.setMapType(google.maps.MapTypeId.SATELLITE)}}/>
    </div>;
  }

  render() {
    let img = window.__STATIC_URL__;
    let solved = this.props.regions.filter(obj => (obj.isSolved)).length;
    return <div className="toolbox-wrapper">
      <div className="toolbox">
        <div className="toolbox-header" onClick={this.toggleCollapse} aria-controls={this.COLLAPSE_ID} aria-expanded={!this.state.collapse}>
          {this.props.wsState !== true &&
            <div id="network-connection-label"><Msg id="networkError"/></div>}
          <Msg id="found"/>: <span>{solved}</span>/<span>{this.props.regions.length}</span>
          <i className={"fas fa-angle-" + (this.state.collapse ? 'up' : 'down')} />
        </div>
        <Collapse in={!this.state.collapse}>
          <div id={this.COLLAPSE_ID}>
            {this.switchMap()}
            <Scrollbars autoHide={true} autoHeight={true} autoHeightMax={this.state.listNameMaxHeight}>
              <ListGroup>
                {this.props.regions.map(polygon => (
                  <NameListItem key={polygon.id} polygon={polygon}
                                click={() => this.props.openInfobox(polygon)}/>
                ))}
              </ListGroup>
            </Scrollbars>
          </div>
        </Collapse>
      </div>
    </div>;
  }
}


export default Toolbox;
