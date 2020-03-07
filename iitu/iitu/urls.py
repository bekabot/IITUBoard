from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include('board.urls')),
]
