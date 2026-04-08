var staticCacheName = "hangarin-v7"; 
var filesToCache = [
    '/', 
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/offline_handler.js',
    '/task/create/', 
    '/static/img/icon-192.png', 
    '/static/img/icon-512.png',
];

self.addEventListener("install", function (e) {
    self.skipWaiting(); 
    e.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return Promise.all(
                filesToCache.map(function(url) {
                    return cache.add(url).catch(err => console.warn("Could not cache:", url));
                })
            );
        })
    );
});

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

    const url = new URL(event.request.url);

    if (url.pathname === '/' || url.pathname.includes('/task/')) {
        event.respondWith(
            fetch(event.request)
                .then(function (response) { 
                    return caches.open(staticCacheName).then(function (cache) {
                        cache.put(event.request, response.clone());
                        return response;
                    });
                })
                .catch(function () {
                    return caches.match(event.request);
                })
        );
        return;
    }

    event.respondWith(
        caches.match(event.request).then(function (response) {
            return response || fetch(event.request);
        })
    );
});