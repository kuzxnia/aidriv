const canvas = document.getElementById("canvas");
const c = canvas.getContext("2d");
let canvas_dimensions, radius;


function getJoyStickPosition() {
    canvas_dimensions = canvas.getBoundingClientRect();
    canvas.width = canvas_dimensions.width;
    canvas.height = canvas_dimensions.height;
    radius = canvas.width / 10;
}

let mouse = {
    x: undefined,
    y: undefined
};

let mouse_down = false;


class JoyStick {
    constructor(x, y, radius, color) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.color = color;
    }

    draw() {
        c.beginPath();
        c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        c.fillStyle = this.color;
        c.globalAlpha = 0.3;
        c.shadowBlur = 15;
        c.shadowColor = "black";
        c.fill();
        c.closePath();
    }
}


let dot = undefined;
function windowSizeChange() {
    getJoyStickPosition();
    dot = new JoyStick(canvas.width / 2, canvas.height / 2, radius, "blue");
}


function animate() {
    c.clearRect(0, 0, canvas.width, canvas.height); // Erase whole canvas
    dot.draw();
    requestAnimationFrame(animate); // Create an animation loop
}


windowSizeChange();
animate();


// Event Listeners
window.addEventListener("load", () => {
    windowSizeChange();
    console.log('load');
    socket.send('resolution ' + resolution.value)
});


window.addEventListener("orientationchange", () => {
    windowSizeChange();
});


window.addEventListener("resize", () => {
    windowSizeChange();
});


let mouse_change = false,
    click_on_canvas = false,
    vertical = 0,
    vertical_old = 0,
    horizontal = 0,
    horizontal_old = 0;


addEventListener("mousemove", event => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
    mouse_change = false;
    if (mouse_down) {
        if (mouse.x >= canvas_dimensions.left && mouse.x <= canvas_dimensions.right && click_on_canvas) {
            horizontal_old = horizontal;
            horizontal = parseInt(((mouse.x - canvas_dimensions.left - canvas.width / 2) / canvas.width) * 200);
            mouse_change = horizontal !== horizontal_old;
            dot.x = mouse.x - canvas_dimensions.left;
        }
        if (mouse.y >= canvas_dimensions.top && mouse.y <= canvas_dimensions.bottom && click_on_canvas) {
            vertical_old = vertical;
            vertical = parseInt((((mouse.y - canvas_dimensions.top - canvas.height / 2) * -1) / canvas.height) * 200);
            mouse_change = vertical !== vertical_old;
            dot.y = mouse.y - canvas_dimensions.top;
        }
        if (mouse_change && click_on_canvas) {
            console.log("goraaa: " + vertical + " bok: " + horizontal);
            socket.send("" + vertical + " " + horizontal);
            if (autonomy_switch.checked) socket.send("ai_false");
            autonomy_switch.checked = false;
        }
    }
});


addEventListener("mousedown", event => {
    mouse_down = true;
    // check if touch was on the canvas and set a flag
    if (
        mouse.x >= canvas_dimensions.left && mouse.x <= canvas_dimensions.right &&
        mouse.y >= canvas_dimensions.top && mouse.y <= canvas_dimensions.bottom
    ) {
        click_on_canvas = true;
    }
});


addEventListener("mouseup", event => {
    if (click_on_canvas) {
        console.log("zatrzymuje pojazd");
        socket.send("0 0");
    }
    click_on_canvas = false;
    mouse_down = false;
    dot.x = canvas.width / 2;
    dot.y = canvas.height / 2;
});


// Mobile event listeners
addEventListener("touchend", event => {
    if (click_on_canvas) {
        console.log("zatrzymuje pojazd");
        socket.send("0 0");
    }
    click_on_canvas = false;
    dot.x = canvas.width / 2;
    dot.y = canvas.height / 2;
});


addEventListener("touchmove", event => {
    mouse_change = false;
    var touches = event.changedTouches;
    // check if touch was on the canvas and set a flag
    if (
        touches[0].clientX >= canvas_dimensions.left && touches[0].clientX <= canvas_dimensions.right &&
        touches[0].clientY >= canvas_dimensions.top && touches[0].clientY <= canvas_dimensions.bottom
    ) {
        click_on_canvas = true;
    }
    if (touches[0].clientX >= canvas_dimensions.left && touches[0].clientX <= canvas_dimensions.right && click_on_canvas) {
        horizontal_old = horizontal;
        horizontal = parseInt(((touches[0].clientX - canvas_dimensions.left - canvas.width / 2) / canvas.width) * 200);
        mouse_change = horizontal !== horizontal_old;
        dot.x = touches[0].clientX - canvas_dimensions.left;
    }
    if (touches[0].clientY >= canvas_dimensions.top && touches[0].clientY <= canvas_dimensions.bottom && click_on_canvas) {
        vertical_old = vertical;
        vertical = parseInt((((touches[0].clientY - canvas_dimensions.top - canvas.height / 2) * -1) / canvas.height) * 200);
        mouse_change = vertical !== vertical_old;
        dot.y = touches[0].clientY - canvas_dimensions.top;
    }
    if (mouse_change) {
        console.log("gora: " + vertical + " bok: " + horizontal);
    	socket.send("" + vertical + " " + horizontal);
        if (autonomy_switch.checked) socket.send("ai_false");
        autonomy_switch.checked = false;
    }
});