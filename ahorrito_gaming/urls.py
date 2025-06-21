from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('core.urls', namespace='core')),
]
# --- CONFIGURACIÓN PARA DESARROLLO ---
# Esta sección es una mejor práctica estándar en Django.
# SOLO se activa cuando DEBUG=True en settings.py.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)