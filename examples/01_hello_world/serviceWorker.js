
const pwa_version = "01_hello_world_202306041650"
const assets = ["./index.html",
    "./main.py",
    "./resources/bootstrap.css",
    "./resources/bootstrap.js",
    "./resources/pyscript.css",
    "./resources/pyscript.js",
    "./resources/pyscript.py",
    "./resources/pyscript_bootstrap_templates-0.2.0-py3-none-any.whl",
    "./resources/pwa.js",
    "./site.js",
]
self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
        caches.open(pwa_version).then(cache => {
            cache.addAll(assets).then(r => {
                console.log("Cache assets downloaded");
            }).catch(err => console.log("Error caching item", err))
            console.log(`Cache ${pwa_version} opened.`);
        }).catch(err => console.log("Error opening cache", err))
    )
})

self.addEventListener('activate', e => {
	console.log('Service Worker: Activated');
});
 
self.addEventListener('fetch', event => {
    if (event.request.method != 'GET')
        return;
	event.respondWith((async () => {
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
            return cachedResponse;
        }

        const response = await fetch(event.request);

        if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
        }

        const responseToCache = response.clone();
        const cache = await caches.open(pwa_version)
        await cache.put(event.request, response.clone());

        return response;
    })());
});
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if(key !== pwa_version) {
                    return caches.delete(key);
                }
            }));
        })
    );
});
    