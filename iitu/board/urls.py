from django.urls import path
from .views import BoardView

from . import views

app_name = "board"

urlpatterns = [
    path('test/', views.index, name='index'),
    path('board/', BoardView.as_view()),
]