const CACHE = 'tnm-v2';
// Path relativi allo scope del service worker: funzionano sia sul sottopercorso
// del progetto GitHub Pages sia su root o sottocartelle diverse senza modifiche.
const ASSETS = [
  './',
  './index.html',
  './index-en.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
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
  if (e.request.method !== 'GET') return;
  const isDoc = e.request.mode === 'navigate' ||
    /\.html$/.test(new URL(e.request.url).pathname);
  if (isDoc) {
    // Network-first per i documenti HTML: contenuto sempre aggiornato, cache fallback offline.
    e.respondWith(
      fetch(e.request)
        .then(r => { caches.open(CACHE).then(c => c.put(e.request, r.clone())); return r; })
        .catch(() => caches.match(e.request).then(m => m || caches.match('./index.html')))
    );
  } else {
    // Cache-first per gli asset statici precaricati (manifest, icone): disponibili offline.
    e.respondWith(
      caches.match(e.request).then(m => m || fetch(e.request).then(r => {
        if (r && r.ok) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
        return r;
      }))
    );
  }
});
