const CACHE = 'tnm-v1';
// Path relativi allo scope del service worker: funzionano sia sul sottopercorso
// del progetto GitHub Pages sia su root o sottocartelle diverse senza modifiche.
const ASSETS = [
  './',
  './index.html',
  './index-en.html'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Network-first solo per i documenti HTML principali, cache fallback offline.
  if (e.request.mode === 'navigate' ||
      /\.html$/.test(new URL(e.request.url).pathname)) {
    e.respondWith(
      fetch(e.request)
        .then(r => { caches.open(CACHE).then(c => c.put(e.request, r.clone())); return r; })
        .catch(() => caches.match(e.request).then(m => m || caches.match('./index.html')))
    );
  }
});
