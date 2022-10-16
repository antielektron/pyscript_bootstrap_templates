
const pwa_version = "202210160801"
const assets = ["/index.html",
    "/main.py",
    "/resources/bootstrap.css",
    "/resources/bootstrap.js",
    "/resources/pyscript.css",
    "/resources/pyscript.js",
    "/resources/pyscript.py",
    "/resources/pyscript_bootstrap_templates-0.1.0-py3-none-any.whl",
    "/resources/pwa.js",
    "/resourced/site.js",
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

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
        caches.match(fetchEvent.request).then(res => {
            return res || fetch(fetchEvent.request)
        }).catch(err => console.log("Cache fetch error: ", err))
    )
})
    