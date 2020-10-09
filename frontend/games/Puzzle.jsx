'use strict';
import React from "react";
import Game from "./Game";
import {decodePolygon, moveTo, prepareInfobox} from "../utils";
import {Button} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";


class Puzzle extends Game {
  GAME_NAME = 'puzzle';

  static extractData(polygons, solved) {
    return polygons.map(country => {
      let paths = decodePolygon(country.polygon);
      return {
        id: country.id,
        draggable: true,
        isSolved: false,
        infobox: {name: country.name, loaded: false},
        paths: moveTo(
          paths,
          new google.maps.LatLng(country.center[1], country.center[0]),
          new google.maps.LatLng(country.default_position[1], country.default_position[0]))
      }
    }).concat(solved.map(region => {
      return {
        id: region.id,
        draggable: false,
        isSolved: true,
        infobox: region.infobox,
        paths: decodePolygon(region.polygon)
      }
    })).sort((one, another) => {
      return one.infobox.name > another.infobox.name ? 1 : -1
    });
  }

  dispatchMessage = (event) => {
    let data = JSON.parse(event.data);
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
              infobox: {...prepareInfobox(data.infobox), loaded: true},
              paths: decodePolygon(data.polygon),
            };
          } else {
            return region;
          }
        });
        infobox = data.infobox;
        break;
      case 'PUZZLE_GIVEUP_DONE':
        regions = regions.map((polygon) => {
          if (!polygon.isSolved) {
            let solve = data.solves[polygon.id];
            return {
              ...polygon,
              draggable: false,
              infobox: {...prepareInfobox(solve.infobox), loaded: true},
              paths: decodePolygon(solve.polygon),
            };
          } else {
            return polygon;
          }
        });
        break;
    }
    this.setState({...this.state, regions: regions, infobox: infobox});
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
    this.wsSend({type: 'PUZZLE_CHECK', coords: coords, id: id, zoom: window.__MAP__.zoom});
    let regions = this.state.regions.map((polygon) => {return (polygon.id === id) ? {...polygon, paths: path} : polygon});
    this.setState({...this.state, regions: regions});
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
