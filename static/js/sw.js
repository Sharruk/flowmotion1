// FlowMotion Service Worker for Push Notifications
const CACHE_NAME = 'flowmotion-v1';

// Install event
self.addEventListener('install', function(event) {
    console.log('[SW] Service Worker installed');
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', function(event) {
    console.log('[SW] Service Worker activated');
    event.waitUntil(self.clients.claim());
});

// Listen for messages from the main page (scheduled notifications)
self.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'SCHEDULE_NOTIFICATION') {
        const { title, body, url, delay } = event.data;
        console.log(`[SW] Scheduling notification "${title}" in ${delay}ms`);
        
        setTimeout(function() {
            self.registration.showNotification(title, {
                body: body,
                icon: '/static/img/flowmotion-icon.png',
                badge: '/static/img/flowmotion-icon.png',
                tag: 'habit-reminder-' + url,
                data: { url: url },
                vibrate: [200, 100, 200],
                requireInteraction: true,
                actions: [
                    { action: 'open', title: '✅ Open Habit' },
                    { action: 'dismiss', title: '❌ Dismiss' }
                ]
            });
        }, delay);
    }
});

// Handle notification click
self.addEventListener('notificationclick', function(event) {
    event.notification.close();

    if (event.action === 'dismiss') {
        return;
    }

    // Open the habit URL
    const url = event.notification.data && event.notification.data.url 
        ? event.notification.data.url 
        : '/dashboard/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function(clientList) {
            // If a window is already open, focus it and navigate
            for (var i = 0; i < clientList.length; i++) {
                var client = clientList[i];
                if (client.url.includes('/dashboard') || client.url.includes('/habits')) {
                    client.navigate(url);
                    return client.focus();
                }
            }
            // Otherwise open a new window
            return clients.openWindow(url);
        })
    );
});
