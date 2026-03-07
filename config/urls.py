from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import contact_view # contact_viewди импорттоп алабыз

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
   path('contact/', contact_view, name='contact'), # Эми дареги: 127.0.0.1:8000/contact/ болот
    path('', include('front.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'front.views.custom_404_view'