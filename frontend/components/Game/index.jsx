'use strict';

import React from "react";
import {render} from "react-dom";
import Loading from "../Loading";
import localization from "../../localization";


class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {isLoaded: null};
    }

    mapInit = () => {};

    mapClick = (e) => {};

    render_loaded() {
        if (this.state.isLoaded === true) {
            return null;
        } else {
            return <Loading text={this.state.isLoaded === null ? localization.loading : 'Something wrong'}/>;
        }
    }

    render() {
        return null;
    };
}

export default Game;