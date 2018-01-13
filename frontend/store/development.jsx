'use strict';
import {createStore, applyMiddleware} from "redux";
import thunkMiddleware from "redux-thunk";
import socketMiddleware from "./socketMiddleware";
import logger from "redux-logger";
import puzzle from '../reducers';


export default function configureStore() {
    return createStore(puzzle, applyMiddleware(thunkMiddleware, logger, socketMiddleware));
}