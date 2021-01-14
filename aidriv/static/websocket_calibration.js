let socket = new WebSocket("ws://" + location.host + "/calibration");

socket.onopen = function(e) {
    console.log("[open] Connection established");
};

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
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


const range1 = document.getElementById("rangeInput1");
const range2 = document.getElementById("rangeInput2");
const range3 = document.getElementById("rangeInput3");
const range4 = document.getElementById("rangeInput4");
const amount1 = document.getElementById("amount1");
const amount2 = document.getElementById("amount2");
const amount3 = document.getElementById("amount3");
const amount4 = document.getElementById("amount4");

function send() {
    socket.send(range1.value + ',' + range2.value + ',' + range3.value + ',' + range4.value)
}

range1.oninput = function() {
    amount1.value=rangeInput1.value
    send()
}

range2.oninput = function() {
    amount2.value=rangeInput2.value
    send()
}

range3.oninput = function() {
    amount3.value=rangeInput3.value
    send()
}

range4.oninput = function() {
    amount4.value=rangeInput4.value
    send()
}

amount1.oninput = function() {
    rangeInput1.value=amount1.value 
    send()
}

amount2.oninput = function() {
    rangeInput2.value=amount2.value 
    send()
}

amount3.oninput = function() {
    rangeInput3.value=amount3.value 
    send()
}

amount4.oninput = function() {
    rangeInput4.value=amount4.value 
    send()
}