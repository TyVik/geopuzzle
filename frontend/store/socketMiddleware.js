import {INIT_LOAD, PUZZLE_CHECK} from "../actions";

const socketMiddleware = (function () {
    let socket = null;
    let addr = null;

    const onOpen = (ws, store) => evt => {
        console.log('connected');
        // store.dispatch(actions.connected());
    };

    const onClose = (ws, store) => evt => {
        console.log('disconnected');
        let reconnect = setInterval(function() {
            console.log('connecting');
            socket = init(socket, store);
            if ((socket.readyState === socket.CONNECTING) || (socket.readyState === socket.OPEN)) {
                clearInterval(reconnect);
            }
        }, 5000);
    };

    const onMessage = (ws, store) => evt => {
        let msg = JSON.parse(evt.data);
        switch (msg.type) {
            case "PUZZLE_CHECK_SUCCESS":
                store.dispatch(msg);
                break;
            default:
                console.log("Received unknown message type: '" + msg.type + "'");
                break;
        }
    };

    const init = (ws, store) => {
        if (ws !== null) {
            ws.close();
        }
        // store.dispatch(actions.connecting());

        ws = new WebSocket(addr);
        ws.onmessage = onMessage(ws, store);
        ws.onclose = onClose(ws, store);
        ws.onopen = onOpen(ws, store);
        return ws;
    };

    return store => next => action => {
        switch (action.type) {
            case INIT_LOAD:
                addr = action.url;
                socket = init(socket, store);
                break;
            case PUZZLE_CHECK:
                socket.send(JSON.stringify(action));
                break;
            default:
                return next(action);
        }
    }
})();

export default socketMiddleware