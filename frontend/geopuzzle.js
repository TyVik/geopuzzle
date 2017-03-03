'use strict';

import React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import Puzzle from './components/Puzzle';
import configureStore from './store';

let store = configureStore();

render(
    <Provider store={store}>
        <Puzzle />
    </Provider>,
    document.getElementById('puzzle')
);