'use strict';

import React from "react";
import {render} from "react-dom";
import Loading from "../Loading";
import localization from "../../localization";
import Congratulation from "../Congratulation";


class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isLoaded: null, congratulation: {show: false, startTime: null}};
    }

    startGame = () => {
        let congrats = {...this.state.congratulation, startTime: Date.now()};
        this.setState({...this.state, isLoaded: true, congratulation: congrats});
    };

    mapInit = () => {};

    mapClick = (e) => {};

    closeCongratulation = () => {
        this.setState({...this.state, congratulation: {...this.state.congratulation, show: false}});
    };

    showCongratulation = () => {
        this.setState({...this.state, congratulation: {...this.state.congratulation, show: true}});
    };

    render_loaded() {
        if (this.state.isLoaded === true) {
            return null;
        } else {
            return <Loading text={this.state.isLoaded === null ? localization.loading : 'Something wrong'}/>;
        }
    }

    render_congratulation() {
        if (this.state.congratulation.show) {
            let time = new Date(Date.now() - this.state.congratulation.startTime);
            let result = (time > 24 * 60 * 60 * 1000) ? 'more then day' : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
            return <Congratulation onClose={this.closeCongratulation} url={location.href} result={result} show={true}/>;
        } else {
            return null;
        }
    }

    render() {
        return null;
    };
}

export default Game;