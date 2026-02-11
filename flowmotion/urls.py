from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponse
import os


def service_worker_view(request):
    """Serve the Service Worker from root scope."""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')
    try:
        with open(sw_path, 'r') as f:
            return HttpResponse(f.read(), content_type='application/javascript')
    except FileNotFoundError:
        return HttpResponse('// SW not found', content_type='application/javascript')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls')),
    path('', include('users.urls')),
    path('api/', include('habits.api_urls')),
    path('sw.js', service_worker_view, name='service_worker'),
]

