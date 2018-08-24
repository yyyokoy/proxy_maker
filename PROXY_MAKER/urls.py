from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('main.urls'), name = 'main'),
    path('card/', include('card_manager.urls'), name = 'card_manager'),
    path('accounts/', include('accounts.urls'), name = 'accounts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
