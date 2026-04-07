var staticCacheName = "hangarin-v2"; // Incremented version to force update
var filesToCache = [
    '/', 
    '/static/img/icon-192.png', 
    '/static/img/icon-512.png',
    // Only include these if you are 100% sure the paths are correct
    // '/static/css/bootstrap.min.css', 
];

// Cache assets on install
self.addEventListener("install", function (e) {
    self.skipWaiting(); // Forces the waiting service worker to become the active one
    e.waitUntil(
        caches.open(staticCacheName).then(function (cache) {
            return cache.addAll(filesToCache);
        }).catch(function(error) {
            console.error('Service Worker: Failed to cache resources:', error);
        })
    );
});

// Remove old caches when a new version is activated
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

// Serve cached content when offline
self.addEventListener("fetch", function (event) {
    event.respondWith(
        caches.match(event.request).then(function (response) {
            // Return cached file, or try to fetch from network
            return response || fetch(event.request).catch(function() {
                // If both fail (offline), you could return an offline page here
                return caches.match('/');
            });
        })
    );
});