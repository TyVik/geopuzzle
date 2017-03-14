'use strict';
import React from "react";
import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';
import {getCountries} from '../../actions';
import Congratulation from '../Congratulation';


class Puzzle extends React.Component {
    mapInit = this.mapInit.bind(this);

    mapInit() {
        return getCountries();
    }

    render() {
        return (
            <div>
                <Loading/>
                <Map initCallback={this.mapInit}/>
                <Infobox/>
                <Toolbox/>
                <Congratulation/>
            </div>
        )
    };
}


export default Puzzle
