from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('core.urls', namespace='core')),
    path('gestion/', include('dashboard.urls', namespace='dashboard')),
    path('', include('core.urls', namespace='core')),
]

# Esta sección es la que permite que las imágenes funcionen cuando DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)