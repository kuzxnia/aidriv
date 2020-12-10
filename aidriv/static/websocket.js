let socket = new WebSocket("ws://" + location.host + "/");

socket.onopen = function(e) {
    console.log("[open] Connection established");
    socket.send('disk_usage')
};

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
    const stats = event.data.split(' ');
    space.max = stats[0];
    space.value = stats[1];
};

socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
        // e.g. server process killed or network down
        // event.code is usually 1006 in this case
        console.log('[close] Connection died');
    }
};

socket.onerror = function(error) {
    console.log(`[error] ${error.message}`);
};
