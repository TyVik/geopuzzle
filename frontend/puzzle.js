'use strict';

import React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import configureStore from './store';
import Map from './components/Map';
import Loading from './components/Loading';
import PuzzleBox from './components/PuzzleBox';
import {INIT_LOAD, INIT_LOAD_FAIL, PUZZLE_INIT_DONE} from './actions';
import Congratulation from './components/Congratulation';


class Puzzle extends React.Component {
    mapInit = this.mapInit.bind(this);
    mapClick = this.mapClick.bind(this);

    mapInit() {
        return (dispatch) => {
            dispatch({type: INIT_LOAD, game: 'puzzle'});
            return fetch(location.pathname.replace('/puzzle/', '/puzzle/questions/') + location.search)
                .then(response => response.json())
                .then(countries => dispatch({type: PUZZLE_INIT_DONE, countries}))
                .catch(response => dispatch({type: INIT_LOAD_FAIL}));
        }
    }

    mapClick(e) {
    }

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <PuzzleBox/>
                <Congratulation/>
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