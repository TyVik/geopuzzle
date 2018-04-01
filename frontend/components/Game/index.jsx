'use strict';

import React from "react";
import {render} from "react-dom";
import Loading from "../Loading";
import localization from "../../localization";
import Congratulation from "../Congratulation";


class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isLoaded: null, startTime: null, regions: [],
            map: {typeId: google.maps.MapTypeId.TERRAIN}, wsState: null};
        this.ws = null;
    }

    startGame = (params) => {
        this.setState({...this.state, ...params, isLoaded: true, startTime: Date.now()});
    };

    mapInit = () => {};

    mapClick = (e) => {};

    render_loaded() {
        if (this.state.isLoaded === true) {
            return null;
        } else {
            return <Loading text={this.state.isLoaded === null ? localization.loading : localization.loadingError}/>;
        }
    }

    render_congratulation() {
        if (this.state.isLoaded && this.state.regions.filter(el => el.isSolved === false).length === 0) {
            let time = new Date(Date.now() - this.state.startTime);
            let result = (time > 24 * 60 * 60 * 1000) ? 'more then day' : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
            return <Congratulation url={location.href} result={result} />;
        } else {
            return null;
        }
    }

    render() {
        return null;
    };
}

export default Game;