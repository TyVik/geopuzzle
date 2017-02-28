import { combineReducers } from 'redux'
import countries from './countries'
import map from './map'
import infobox from './infobox'

const puzzle = combineReducers({
    countries,
    map,
    infobox
});

export default puzzle