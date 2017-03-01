import { combineReducers } from 'redux'
import countries from './countries'
import map from './map'
import infobox from './infobox'
import congratulation from './congratulation'

const puzzle = combineReducers({
    countries,
    map,
    infobox,
    congratulation
});

export default puzzle