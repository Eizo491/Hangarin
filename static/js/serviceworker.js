var staticCacheName = "hangarin-v5"; // Bump to v5 to force a fresh start
var filesToCache = [
    '/', 
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

// Serve cached content - FIXED LOGIC
self.addEventListener("fetch", function (event) {
    // Skip cross-origin requests (like Google Fonts or APIs) to avoid errors
    if (!event.request.url.startsWith(self.location.origin)) return;

    event.respondWith(
        caches.match(event.request).then(function (response) {
            // 1. If it's in cache, return it
            if (response) return response;

            // 2. If not, try the network
            return fetch(event.request).catch(function() {
                // 3. Only if BOTH fail, try to return the cached home page as a fallback
                return caches.match('/');
            });
        })
    );
});