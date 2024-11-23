from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from callboard.views import user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ads/', include('callboard.urls')),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', user_profile, name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
