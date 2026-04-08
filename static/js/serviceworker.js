var staticCacheName = "hangarin-v6"; // Bumped to v6 to include offline handler scripts
var filesToCache = [
    '/', 
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/offline_handler.js',
    '/task/create/', // Ensure your "Add Task" URL is cached so the form opens offline
    '/static/img/icon-192.png', 
    '/static/img/icon-512.png',
];

// Cache assets on install
self.addEventListener("install", function (e) {
    self.skipWaiting(); 
    e.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            // We use a map to try caching files individually so one failure doesn't kill the worker
            return Promise.all(
                filesToCache.map(function(url) {
                    return cache.add(url).catch(err => console.warn("Could not cache:", url));
                })
            );
        })
    );
});

// Remove old caches
self.addEventListener("activate", function (e) {
    e.waitUntil(
        caches.keys().then(function (cacheNames) {
            return Promise.all(
                cacheNames.map(function (thisCacheName) {
                    if (thisCacheName !== staticCacheName) {
                        return caches.delete(thisCacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener("fetch", function (event) {
    if (!event.request.url.startsWith(self.location.origin)) return;

    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then(function (response) {
            if (response) return response;

            return fetch(event.request).then(function(networkResponse) {
                return networkResponse;
            }).catch(function() {
                return caches.match('/');
            });
        })
    );
});