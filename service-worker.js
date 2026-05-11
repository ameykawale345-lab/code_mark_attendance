const CACHE_NAME = 'smartattend-v2';
const ASSETS = ['./', './index.html', './manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  const apiRoutes = ['/register','/login','/verify','/resend-otp','/student/','/teacher/','/admin/'];
  if (apiRoutes.some(r => url.pathname.startsWith(r))) {
    e.respondWith(fetch(e.request).catch(() =>
      new Response(JSON.stringify({message:'You are offline'}),
        {headers:{'Content-Type':'application/json'}})
    ));
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
