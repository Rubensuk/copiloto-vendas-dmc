const CACHE_NAME = 'dmc-copilot-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/simulador.html',
  'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('fetch', event => {
  // Para a API (CSV do Google), tentamos a rede primeiro, depois o cache
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

  // Para HTML, CSS e JS (assets estáticos), cache primeiro, fallback para rede
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
