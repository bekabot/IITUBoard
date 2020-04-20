from django.urls import path

from .views import BoardView, LoginView, AuthView, VerificationView, RestoreView, ComplaintsView

app_name = "board"

urlpatterns = [
    path('board/', BoardView.as_view()),
    path('login/', LoginView.as_view()),
    path('auth/', AuthView.as_view()),
    path('verify/', VerificationView.as_view()),
    path('restore/', RestoreView.as_view()),
    path('complaints/', ComplaintsView.as_view()),
]
