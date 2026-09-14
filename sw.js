const CACHE_NAME = 'dmc-copilot-v2';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/simulador.html',
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap'
];

self.addEventListener('install', event => {
  // Force new service worker to activate immediately
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('activate', event => {
  // Take control immediately and delete old caches
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.map(key => {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      })
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // Para a API (CSV do Google), Network first, fallback para cache
  if (event.request.url.includes('/api/sheet')) {
    event.respondWith(
      fetch(event.request).then(response => {
        const clonedResponse = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clonedResponse));
        return response;
      }).catch(() => caches.match(event.request))
    );
    return;
  }

  // Para arquivos HTML, Network First para sempre ter a versão mais recente!
  if (event.request.mode === 'navigate' || event.request.headers.get('accept').includes('text/html')) {
      event.respondWith(
          fetch(event.request).then(response => {
              const clonedResponse = response.clone();
              caches.open(CACHE_NAME).then(cache => cache.put(event.request, clonedResponse));
              return response;
          }).catch(() => caches.match(event.request))
      );
      return;
  }

  // Para outros assets estáticos (Stale-While-Revalidate)
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      const fetchPromise = fetch(event.request).then(networkResponse => {
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, networkResponse.clone()));
        return networkResponse;
      }).catch(() => {});
      return cachedResponse || fetchPromise;
    })
  );
});
