'use strict';

import React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import configureStore from './store';
import Map from './components/Map';
import PuzzleBox from './components/PuzzleBox';
import {INIT_LOAD, PUZZLE_INIT_DONE} from './actions';
import Game from "./components/Game";


class Puzzle extends Game {
    mapInit = () => {
        return (dispatch) => {
            dispatch({type: INIT_LOAD, game: 'puzzle'});
            return fetch(location.pathname.replace('/puzzle/', '/puzzle/questions/') + location.search)
                .then(response => response.json())
                .then(countries => {
                    dispatch({type: PUZZLE_INIT_DONE, ...countries});
                    this.startGame();
                })
                .catch(response => {this.setState({...this.state, isLoaded: false})});
        }
    };

    render() {
        return (
            <div>
                {this.render_loaded()}
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <PuzzleBox showCongrats={this.showCongratulation}/>
                {this.render_congratulation()}
            </div>
        )
    };
}


let store = configureStore();

render(
    <Provider store={store}>
        <Puzzle />
    </Provider>,
    document.getElementById('puzzle')
);