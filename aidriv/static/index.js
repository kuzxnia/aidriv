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