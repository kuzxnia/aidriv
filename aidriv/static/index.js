window.addEventListener("load", () => {
    registerSW();
});

async function registerSW() {
    if ("serviceWorker" in navigator) {
        try {
            await navigator.serviceWorker.register("./sw.js");
        } catch (e) {
            console.log(`SW registration failed`);
        }
    }
}

document.getElementById("camera").src = "http://" + location.host + "/video_feed";

const picture = document.getElementById("picture");
const resolution = document.getElementById("resolution");
const video = document.getElementById("video");
const recording = document.getElementById("recording");
const camera = document.getElementById("camera");
const space = document.getElementById("space");
const autonomy_switch = document.getElementById("myonoffswitch");


picture.onclick = function() {
    camera.classList.remove('take-picture');
    camera.offsetWidth;
    socket.send('take_pic')
    camera.classList.add('take-picture');
}


resolution.onchange = function() {
    socket.send('resolution ' + resolution.value)
}


video.onclick = function() {
    socket.send(video.value)
    if (video.value === "start_video") {
        recording.style.visibility = 'visible';
        video.value = 'stop_video';
        timer();
    } else {
        recording.style.visibility = 'hidden';
        video.value = 'start_video';
        clearTimeout(t);
        p.textContent = "00:00:00";
        seconds = 0; minutes = 0; hours = 0;
    }
    if (video.classList.contains('start_video')) {
        video.classList.remove('start_video');
        video.classList.remove('fa-video');
        video.classList.add('stop_video');
        video.classList.add('fa-stop');
    } else {
        video.classList.remove('stop_video');
        video.classList.remove('fa-stop');
        video.classList.add('start_video');
        video.classList.add('fa-video');
    }
}


autonomy_switch.addEventListener('change', (event) => {
    if (autonomy_switch.checked) {
        socket.send("ai_true");
        console.log("ai_true");
    } else {
        socket.send("ai_false");
        console.log("ai_false");
    }
});


function disk_usage() {
    socket.send('disk_usage')
}

var t = setInterval(disk_usage, 100000)