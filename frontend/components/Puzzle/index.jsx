'use strict';
import React from "react";
import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';
import {INIT_LOAD, INIT_LOAD_FAIL, INIT_PUZZLE_DONE} from '../../actions';
import Congratulation from '../Congratulation';


class Puzzle extends React.Component {
    mapInit = this.mapInit.bind(this);
    mapClick = this.mapClick.bind(this);

    mapInit() {
        return (dispatch) => {
            dispatch({type: INIT_LOAD});
            return fetch(location.pathname.replace('/maps/', '/maps/questions/') + location.search)
                .then(response => response.json())
                .then(countries => dispatch({type: INIT_PUZZLE_DONE, countries}))
                .catch(response => dispatch({type: INIT_LOAD_FAIL}));
        }
    }

    mapClick(e) {}

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit} mapClick={this.mapClick}/>
                <Infobox/>
                <Toolbox/>
                <Congratulation/>
            </div>
        )
    };
}


export default Puzzle
