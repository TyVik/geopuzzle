'use strict';
import {
    GET_INFOBOX_DONE, PUZZLE_INIT_DONE, QUIZ_INIT_DONE, QUIZ_GIVEUP_DONE,
    PUZZLE_CHECK_SUCCESS, DRAG_END_POLYGON, QUIZ_CHECK_SUCCESS,
    PUZZLE_GIVEUP_DONE, prepareInfobox
} from "../actions";


function moveTo(paths, from, to) {
    let polygon = new google.maps.Polygon({geodesic: true, paths: paths});
    polygon.moveTo(from, to);
    return polygon.getPaths();
}


function decodePolygon(polygon) {
    return polygon.map(polygon => (google.maps.geometry.encoding.decodePath(polygon)));
}

function extractForPuzzle(countries) {
    return countries.map(country => {
        let paths = decodePolygon(country.polygon);
        return {
            id: country.id,
            draggable: true,
            isSolved: false,
            infobox: {name: country.name, loaded: false},
            paths: moveTo(
                paths,
                new google.maps.LatLng(country.center[1], country.center[0]),
                new google.maps.LatLng(country.default_position[1], country.default_position[0]))
        }
    }).sort((one, another) => {
        return one.infobox.name > another.infobox.name ? 1 : -1
    });
}

function extractForQuiz(polygons, founded) {
    return polygons.map(polygon => {
        return {
            id: polygon.id,
            draggable: true,
            isSolved: false,
            infobox: {name: polygon.name, loaded: false},
            paths: []
        }
    }).concat(founded.map(region => {
        return {
            id: region.id,
            draggable: false,
            isSolved: true,
            infobox: region.infobox,
            paths: decodePolygon(region.polygon)
        }
    })).sort((one, another) => {
        return one.infobox.name > another.infobox.name ? 1 : -1
    });
}

const polygons = (state = [], action) => {
    switch (action.type) {
        case GET_INFOBOX_DONE:
            return state.map((country) => {
                if (country.id === action.id) {
                    let data = prepareInfobox(action.infobox);
                    return {...country, infobox: {...data, loaded: true}};
                }
                return country
            });
        case QUIZ_CHECK_SUCCESS:
        case QUIZ_GIVEUP_DONE:
            let infobox = prepareInfobox(action.infobox);
            return state.map((polygon) => {
                if (polygon.id === action.id) {
                    return {
                        draggable: false,
                        id: action.id,
                        isSolved: action.type === QUIZ_CHECK_SUCCESS,
                        infobox: {...infobox, loaded: true},
                        paths: decodePolygon(action.polygon)
                    };
                }
                return polygon
            });
        case PUZZLE_INIT_DONE:
            return extractForPuzzle(action.countries);
        case QUIZ_INIT_DONE:
            return extractForQuiz(action.questions, action.founded);
        case PUZZLE_GIVEUP_DONE:
            return state.map((polygon) => {
                if (!polygon.isSolved) {
                    let solve = action.solves[polygon.id];
                    return {
                        ...polygon,
                        draggable: false,
                        infobox: prepareInfobox(solve.infobox),
                        paths: decodePolygon(solve.polygon),
                    };
                }
                return polygon
            });
        case DRAG_END_POLYGON:
            return state.map((polygon) => {
                if (polygon.id === action.id) {
                    return {...polygon, paths: action.paths};
                }
                return polygon
            });
        case PUZZLE_CHECK_SUCCESS:
            return state.map((polygon) => {
                if (polygon.id === action.id) {
                    return {
                        ...polygon,
                        draggable: false,
                        isSolved: true,
                        infobox: prepareInfobox(action.infobox),
                        paths: decodePolygon(action.polygon),
                    };
                }
                return polygon
            });
        default:
            return state
    }
};


export default polygons