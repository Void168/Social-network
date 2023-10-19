from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from account.views import activate_email


urlpatterns = [
    path('api/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('api/search/', include('search.urls')),
    path('api/posts/', include('post.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notification.urls')),
    path('activate-email/', activate_email, name='activate_email')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
