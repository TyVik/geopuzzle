import React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import {createStore, applyMiddleware} from "redux";
import thunkMiddleware from "redux-thunk";
import createLogger from "redux-logger";
import puzzle from './reducers';
import Puzzle from './components/Puzzle';

const logger = createLogger();

let store = createStore(puzzle, applyMiddleware(thunkMiddleware, logger));

render(
    <Provider store={store}>
        <Puzzle />
    </Provider>,
    document.getElementById('puzzle')
);