'use strict';
import { combineReducers } from 'redux'
import map from './map'
import quiz from './quiz'
import infobox from './infobox'
import polygons from './polygons'

const puzzle = combineReducers({
    polygons,
    map,
    infobox,
    quiz,
});

export default puzzle;
