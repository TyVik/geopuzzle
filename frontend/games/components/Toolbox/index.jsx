'use strict';
/* global google */
import React from "react";
import {Collapse} from "react-bootstrap";
import { Scrollbars } from 'react-custom-scrollbars';
import ListGroup from "react-bootstrap/ListGroup";
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";


const NameListItem = (props) => {
  if (!props.polygon.draggable) {
    return <ListGroup.Item variant={props.polygon.isSolved ? 'success' : 'danger'} onClick={props.click} action={true}>
      {props.polygon.infobox.name}
    </ListGroup.Item>;
  } else {
    return <ListGroup.Item variant="danger">&nbsp;</ListGroup.Item>;
  }
};


class Toolbox extends React.Component {
  COLLAPSE_ID = 'toolbox-collapse';

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
    return <div className="toolbox-wrapper">
      <div className="toolbox">
        <div className="toolbox-header" onClick={this.toggleCollapse} aria-controls={this.COLLAPSE_ID} aria-expanded={!this.state.collapse}>
          {this.props.wsState !== true &&
            <div id="network_connection_label"><Msg id="networkError"/></div>}
          <Msg id="found"/>: <span>{solved}</span>/<span>{this.props.regions.length}</span>
          <i className={"fas fa-angle-" + (this.state.collapse ? 'up' : 'down')} />
        </div>
        <Collapse in={!this.state.collapse}>
          <div id={this.COLLAPSE_ID}>
            <div className="map_switcher_wrapper">
              <img className="map_switcher" src={img + "images/map/terrain.png"}
                   onClick={() => {this.props.setMapType(google.maps.MapTypeId.TERRAIN)}}/>
              <img className="map_switcher" src={img + "images/map/hybrid.png"}
                   onClick={() => {this.props.setMapType(google.maps.MapTypeId.HYBRID)}}/>
              <img className="map_switcher" src={img + "images/map/satellite.png"}
                   onClick={() => {this.props.setMapType(google.maps.MapTypeId.SATELLITE)}}/>
            </div>
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
