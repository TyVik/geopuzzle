import {INIT_LOAD} from "../actions";

const socketMiddleware = (function () {
    let socket = null;
    let addr = null;

    const onOpen = (ws, store) => evt => {
        console.log('connected');
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
        store.dispatch(JSON.parse(evt.data));
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
        if (action.type === INIT_LOAD) {
            addr = action.url;
            socket = init(socket, store);
        } else {
            if (action.ws) {
                socket.send(JSON.stringify(action));
            } else {
                return next(action);
            }
        }
    }
})();

export default socketMiddleware