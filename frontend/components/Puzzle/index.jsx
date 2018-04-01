'use strict';
import React from "react";
import {render} from "react-dom";
import Sockette from 'sockette';
import Map from '../Map';
import {PUZZLE_CHECK, PUZZLE_CHECK_SUCCESS, PUZZLE_GIVEUP, PUZZLE_GIVEUP_DONE} from '../../actions';
import Game from "../Game";
import {decodePolygon, moveTo, prepareInfobox} from "../../utils";
import localization from "../../localization";


import './index.css';
import Toolbox from "../Toolbox";
import Button from "react-bootstrap/es/Button";
import Infobox from "../Infobox";


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
        switch(data.type) {
            case PUZZLE_CHECK_SUCCESS:
                let regions = this.state.regions.map((region) => {
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
                this.setState({...this.state, regions: regions, infobox: data.infobox});
                break;
            case PUZZLE_GIVEUP_DONE:
                let regions1 = this.state.regions.map((polygon) => {
                    if (!polygon.isSolved) {
                        let solve = data.solves[polygon.id];
                        return {
                            ...polygon,
                            draggable: false,
                            infobox: prepareInfobox(solve.infobox),
                            paths: decodePolygon(solve.polygon),
                        };
                    } else {
                        return polygon;
                    }
                });
                this.setState({...this.state, regions: regions1});
                break;
        }
    };

    mapInit = () => {
        fetch(location.pathname.replace('/puzzle/', '/puzzle/questions/') + location.search)
            .then(response => response.json())
            .then(data => {
                let regions = Puzzle.extractData(data.questions, data.solved);
                let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
                let addr = ws_scheme + '://' + window.location.host + '/ws/' + this.GAME_NAME + '/';
                this.ws = new Sockette(addr, {
                    timeout: 5e3,
                    maxAttempts: 10,
                    onopen: e => this.setState({...this.state, wsState: true}),
                    onmessage: e => this.dispatchMessage(e),
                    onreconnect: e => this.setState({...this.state, wsState: null}),
                    onmaximum: e => this.setState({...this.state, wsState: false}),
                    onclose: e => this.setState({...this.state, wsState: null}),
                    onerror: e => this.setState({...this.state, wsState: false})
                });
                this.startGame(regions);
            })
            .catch(response => {
                console.log(response);
                this.setState({...this.state, isLoaded: false})
            });
    };

    giveUp = () => {
        let ids = this.state.regions.filter(obj => (!obj.isSolved)).map(polygon => (polygon.id));
        return this.ws.json({ids: ids, type: PUZZLE_GIVEUP});
    };

    setMapType = (typeId) => {
        let map = {...this.state.map, typeId: typeId};
        this.setState({...this.state, map: map});
    };

    onPolygonClick = (polygon) => {
        if (polygon && !polygon.draggable) {
            let region = this.state.regions.find(x => x.id === polygon.id);
            if (region.infobox.loaded) {
                this.setState({...this.state, infobox: region.infobox});
            } else {
                let id = region.id;
                fetch(window.location.origin + `/puzzle/area/` + region.id + '/infobox/')
                    .then(response => response.json())
                    .then(json => {
                        let regions = this.state.regions.map((region) => {
                            if (region.id === id) {
                                return {
                                    ...region,
                                    infobox: prepareInfobox(json),
                                };
                            } else {
                                return region;
                            }
                        });
                        this.setState({...this.state, regions: regions, infobox: prepareInfobox(json)});
                    })
                    .catch(response => console.log(response));
            }
        }
    };

    onDragEnd = (coords, id) => {
        this.ws.json({type: PUZZLE_CHECK, coords: coords, id: id, zoom: window.__MAP__.zoom});
    };

    showInfobox = (region) => {

    };

    render() {
        return (
            <div>
                {this.render_loaded()}
                <Map initCallback={this.mapInit} mapClick={this.mapClick} mapTypeId={this.state.map.typeId}
                     regions={this.state.regions} onPolygonClick={this.onPolygonClick} onDragEnd={this.onDragEnd}/>
                <div className="puzzle-box">
                    <Toolbox setMapType={this.setMapType} regions={this.state.regions} wsState={this.state.wsState}
                             showInfobox={this.showInfobox}/>
                    <Button bsStyle="success" onClick={this.giveUp}>
                        {localization.give_up}
                    </Button>
                    <div className="infobox-wrapper">
                        <Infobox {...this.state.infobox} show={true}/>
                    </div>
                </div>
                {this.render_congratulation()}
            </div>
        )
    };
}


export default Puzzle;