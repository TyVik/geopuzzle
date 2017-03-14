'use strict';

import React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import Quiz from './components/Quiz';
import configureStore from './store';

let store = configureStore();

render(
    <Provider store={store}>
        <Quiz />
    </Provider>,
    document.getElementById('quiz')
);