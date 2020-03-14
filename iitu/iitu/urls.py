from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include('board.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
