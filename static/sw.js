const cacheName = "aidriv";
const staticAssets = [
    "/sw.js",
    "/manifest.json",
    "/fallback.html",
    "/style.css",
    "/images/aidriv.png",
    "/images/icon-512x512.png",
    "/images/icon-192x192.png"
];

self.addEventListener("install", event => {
    console.log('install');
    event.waitUntil(
        caches.open(cacheName).then(cache => {
            cache.addAll(staticAssets);
        })
    );
});

self.addEventListener("activate", e => {
    self.clients.claim();
});

self.addEventListener("fetch", event => {
    self.skipWaiting();
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        }).catch(() => {
            return caches.match("/fallback.html");
        })
    );
});