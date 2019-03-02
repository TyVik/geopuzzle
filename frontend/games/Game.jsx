'use strict';
import React from "react";
import Loading from "../components/Loading/index";
import Sockette from './ws';
import Congratulation from "./components/Congratulation/index";
import {prepareInfobox} from "../utils";
import Toolbox from "./components/Toolbox/index";
import Infobox from "./components/Infobox/index";
import Map from '../components/Map/index';
import {FormattedMessage as Msg} from "react-intl";


import './index.css';


class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {isLoaded: null, startTime: null, regions: [], showInfobox: true, infobox: null,
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

  startGame = (params) => {
    let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    let addr = ws_scheme + '://' + window.location.host + '/ws/' + this.GAME_NAME + '/';
    this.ws = new Sockette(addr, {
      timeout: 5e3,
      onopen: e => this.setState({...this.state, wsState: true}),
      onmessage: e => this.dispatchMessage(e),
      onreconnect: e => this.setState({...this.state, wsState: null}),
      onmaximum: e => this.setState({...this.state, wsState: false}),
      onclose: e => this.setState({...this.state, wsState: null}),
      onerror: e => this.setState({...this.state, wsState: false})
    });
    this.setState({...this.state, ...params, isLoaded: true, startTime: Date.now()});
  };

  mapInit = () => {};

  mapClick = (e) => {};

  setMapType = (typeId) => {
    let map = {...this.state.map, typeId: typeId};
    this.setState({...this.state, map: map});
  };

  closeInfobox = () => {
    this.setState({...this.state, showInfobox: false});
  };

  openInfobox = (region) => {
    this.setState({...this.state, showInfobox: true, infobox: region.infobox});
  };

  onPolygonClick = (polygon) => {
    if (polygon && (polygon.draggable !== undefined) && !polygon.draggable) {
      let region = this.state.regions.find(x => x.id === polygon.id);
      if (region.infobox.loaded) {
        this.setState({...this.state, infobox: region.infobox, showInfobox: true});
      } else {
        let id = region.id;
        fetch(window.location.origin + `/puzzle/area/${region.id}/infobox/`)
          .then(response => response.json())
          .then(json => {
            let regions = this.state.regions.map((region) =>
              region.id === id ? {...region, infobox: prepareInfobox(json)} : region);
            this.setState({...this.state, regions: regions, infobox: json, showInfobox: true});
          })
          .catch(response => console.log(response));
      }
    }
  };

  render_loaded() {
    return this.state.isLoaded === true ? null :
      <Loading hasError={this.state.isLoaded !== null}/>;
  }

  render_congratulation() {
    if (this.state.regions.length > 0 && this.state.regions.filter(el => el.isSolved === false).length === 0) {
      let time = new Date(Date.now() - this.state.startTime);
      let result = (time > 24 * 60 * 60 * 1000) ? <Msg id="timeOverhead"/> : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
      return <Congratulation url={location.href} result={result} />;
    } else {
      return null;
    }
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
           onPolygonClick={this.onPolygonClick} onDragPolygon={this.onDragPolygon}/>
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
