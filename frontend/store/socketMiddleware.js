import {INIT_LOAD} from "../actions";

const socketMiddleware = (function () {
    let socket = null;
    let addr = null;

    const onOpen = (ws, store) => evt => {
        console.log('connected');
        let message = document.getElementById('network_connection_label');
        message.className = 'hide';
    };

    const onClose = (ws, store) => evt => {
        console.log('disconnected');
        let message = document.getElementById('network_connection_label');
        message.className = 'show';
        let reconnect = setInterval(function() {
            console.log('connecting');
            socket = init(socket, store);
            if ((socket.readyState === socket.CONNECTING) || (socket.readyState === socket.OPEN)) {
                clearInterval(reconnect);
            }
        }, 3000);
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

    const waitForSocketConnection = (socket, callback) => {
        setTimeout(() => {
            if (socket.readyState === socket.OPEN) {
                callback();
            } else {
                waitForSocketConnection(socket, callback);
            }
        }, 10);
    };

    return store => next => action => {
        if (action.type === INIT_LOAD) {
            let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
            addr = ws_scheme + '://' + window.location.host + '/ws/' + action.game + '/';
            socket = init(socket, store);
        } else {
            if (action.ws) {
                waitForSocketConnection(socket, () => { socket.send(JSON.stringify(action)); });
            } else {
                return next(action);
            }
        }
    }
})();

export default socketMiddleware