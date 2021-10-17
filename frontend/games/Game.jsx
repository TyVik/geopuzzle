'use strict';
import React from "react";
import Loading from "../components/Loading/index";
import Sockette from './ws';
import {prepareInfobox} from "../utils";
import Toolbox from "./components/Toolbox/index";
import Infobox from "./components/Infobox/index";
import Map from '../components/Map/index';
import {Congratulation} from "./components/Congratulation";

import './index.css';


class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isLoaded: null, startTime: null, regions: [], showInfobox: true, infobox: null,
      congratulations: null,
      map: {typeId: google.maps.MapTypeId.TERRAIN}, wsState: null, showMap: true};
    this.ws = null;
  }

  wsSend = (payload) => {
    if(this.ws && this.ws.isReady() === 1) {
      this.ws.json(payload);
    } else {
      setTimeout(() => {this.wsSend(payload);}, 100);
    }
  };

  setupWs = () => {
    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let addr = `${ws_scheme}://${window.location.host}/ws/${this.GAME_NAME}/`;
    this.ws = new Sockette(addr, {
      timeout: 5e3,
      onopen: e => this.setState(state => ({...state, wsState: true})),
      onmessage: e => this.dispatchMessage(e),
      onreconnect: e => this.setState(state => ({...state, wsState: null})),
      onmaximum: e => this.setState(state => ({...state, wsState: false})),
      onclose: e => this.setState(state => ({...state, wsState: null})),
      onerror: e => this.setState(state => ({...state, wsState: false}))
    });
  };

  startGame = (params) => {
    this.setState(state => ({...state, ...params, isLoaded: true, startTime: Date.now()}));
  };

  dispatchMessage = (event) => {
    let data = JSON.parse(event.data);
    this._dispatchMessage(data);
    if (this.state.regions.every(obj => obj.isSolved)) {
      let score = new Date(Date.now() - this.state.startTime).getSeconds();
      this.setState(state => ({...state, congratulations: {score: score}}));
    }
  };

  _dispatchMessage = (data) => {};

  mapInit = () => {
    this.setupWs();
    this.loadData();
  };

  loadData = () => {};

  mapClick = (e) => {};

  setMapType = (typeId) => {
    this.setState(state => ({...state, map: {...state.map, typeId: typeId}}));
  };

  closeInfobox = () => {
    this.setState(state => ({...state, showInfobox: false}));
  };

  openInfobox = (region) => {
    this.setState(state => ({...state, showInfobox: true, infobox: region.infobox}));
  };

  onPolygonClick = async (polygon) => {
    if (polygon && (polygon.draggable !== undefined) && !polygon.draggable) {
      let region = this.state.regions.find(x => x.id === polygon.id);
      if (region.infobox.loaded) {
        this.openInfobox(region);
      } else {
        let id = region.id;
        try {
          let response = await fetch(`${window.location.origin}/puzzle/area/${id}/infobox/`, {method: 'GET'});
          let data = await response.json();
          let regions = this.state.regions.map((region) =>
            region.id === id ? {...region, infobox: prepareInfobox(data)} : region);
          this.setState(state => ({...state, regions: regions, infobox: data, showInfobox: true}));
        } catch (e) {
          console.log(e);
        }
      }
    }
  };

  render_loaded() {
    return this.state.isLoaded === true ? null : <Loading hasError={this.state.isLoaded !== null}/>;
  }

  render_congratulation() {
    if ((this.state.isLoaded) && (this.state.congratulations)) {
      return <Congratulation text={`congratulations.${this.GAME_NAME}`} options={this.state.congratulations}
                             name={this.props.game.name} subjects={this.props.game.parts}/>;
    }
    return null;
  }

  render_question() {
    return null;
  }

  render_popup() {
    return null;
  }

  render() {
    return <div>
      {this.render_loaded()}
      <Map initCallback={this.mapInit} mapClick={this.mapClick} mapTypeId={this.state.map.typeId}
           infobox={this.state.infobox} regions={this.state.regions} showMap={this.state.showMap}
           onPolygonClick={this.onPolygonClick} onDragPolygon={this.onDragPolygon} map={this.props.map}/>
      {this.render_popup()}
      <div className="game-box">
        <Toolbox setMapType={this.setMapType} regions={this.state.regions} wsState={this.state.wsState}
                 openInfobox={this.openInfobox} />
        {this.render_question()}
        <div className="infobox-wrapper">
          <Infobox {...this.state.infobox} show={this.state.showInfobox && (this.state.infobox !== null)}
                   onClose={this.closeInfobox}/>
        </div>
      </div>
      {this.render_congratulation()}
    </div>;
  };
}

export default Game;
