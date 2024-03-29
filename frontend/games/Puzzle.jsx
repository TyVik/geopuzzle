'use strict';
import React from "react";
import Game from "./Game";
import { prepareInfobox } from "./utils";
import {Button} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";
import Map from "../components/Map";


class Puzzle extends Game {
  GAME_NAME = 'puzzle';

  static extractData(polygons, solved) {
    return polygons.map(country => {
      let paths = Map.preparePolygon(country.polygon, true);
      paths = Map.moveTo(paths, country.center, country.default_position);
      return {
        id: country.id,
        draggable: true,
        isSolved: false,
        isOpen: false,
        defaultPosition: country.default_position,
        infobox: {name: country.name, loaded: false},
        paths: paths
      }
    }).concat(solved.map(region => {
      return {
        id: region.id,
        draggable: false,
        isSolved: true,
        isOpen: true,
        infobox: region.infobox,
        paths: Map.preparePolygon(region.polygon)
      }
    })).sort((one, another) => {
      return one.infobox.name > another.infobox.name ? 1 : -1
    });
  }

  _dispatchMessage = (data) => {
    let regions = this.state.regions;
    let infobox = this.state.infobox;
    switch(data.type) {
      case 'PUZZLE_CHECK_SUCCESS':
        regions = regions.map((region) => {
          if (region.id === data.id) {
            return {
              ...region,
              draggable: false,
              isSolved: true,
              isOpen: true,
              infobox: {...prepareInfobox(data.infobox), loaded: true},
              paths: Map.preparePolygon(data.polygon),
            };
          } else {
            return region;
          }
        });
        infobox = data.infobox;
        this.setState(state => ({...state, regions: regions, infobox: infobox}));
        break;
      case 'PUZZLE_GIVEUP_DONE':
        regions = regions.map((polygon) => {
          if (!polygon.isSolved) {
            let solve = data.solves[polygon.id];
            return {
              ...polygon,
              draggable: false,
              isOpen: true,
              infobox: {...prepareInfobox(solve.infobox), loaded: true},
              paths: Map.preparePolygon(solve.polygon),
            };
          } else {
            return polygon;
          }
        });
        this.setState(state => ({...state, regions: regions, infobox: infobox}));
        break;
    }
  };

  loadData = () => {
    fetch(`${location.pathname}questions/${location.search}`)
      .then(response => response.json())
      .then(data => {
        this.startGame({regions: Puzzle.extractData(data.questions, data.solved)});
      })
      .catch(response => {
        this.setState({...this.state, isLoaded: false})
      });
  };

  giveUp = () => {
    let ids = this.state.regions.filter(obj => (!obj.isSolved)).map(polygon => (polygon.id));
    return this.wsSend({ids: ids, type: 'PUZZLE_GIVEUP'});
  };

  refreshMap = () => {
    this.setState({...this.state, showMap: false}, () => {this.setState({...this.state, showMap: true})});
  };

  onDragPolygon = (id, coords, path) => {
    this.wsSend({type: 'PUZZLE_CHECK', coords: coords, id: id, zoom: this.props.map.zoom});
  };

  render_question() {
    return <div className="text-center">
      <Button variant="primary" onClick={this.giveUp} className="mx-2">
        <Msg id="giveUp"/>
      </Button>
      <Button variant="warning" onClick={this.refreshMap} className="mx-2">
        <Msg id="fixProblem"/>
      </Button>
    </div>;
  }
}


export default Puzzle;
