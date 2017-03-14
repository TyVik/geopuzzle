'use strict';
import { combineReducers } from 'redux'
import map from './map'
import quiz from './quiz'
import infobox from './infobox'
import polygons from './polygons'
import congratulation from './congratulation'

const puzzle = combineReducers({
    congratulation,
    polygons,
    map,
    infobox,
    quiz,
});

export default puzzle