import {SHOW_CONGRATULATION, CLOSE_CONGRATULATION} from '../actions';


let init = {show: false, text: ''};

const congratulation = (state = init, action) => {
    switch (action.type) {
        case CLOSE_CONGRATULATION:
            return init;
        case SHOW_CONGRATULATION:
            return {show: true, text: action.text};
        default:
            return state
    }
};


export default congratulation
