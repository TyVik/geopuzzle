'use strict';
import {createStore, applyMiddleware} from "redux";
import thunkMiddleware from "redux-thunk";
import createLogger from "redux-logger";
import puzzle from '../reducers';


export default function configureStore() {
    const logger = createLogger();
    return createStore(puzzle, applyMiddleware(thunkMiddleware, logger));
}