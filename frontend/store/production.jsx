'use strict';
import {createStore, applyMiddleware} from "redux";
import thunkMiddleware from "redux-thunk";
import socketMiddleware from "./socketMiddleware";
import puzzle from "../reducers";


export default function configureStore() {
    return createStore(puzzle, applyMiddleware(thunkMiddleware, socketMiddleware));
}