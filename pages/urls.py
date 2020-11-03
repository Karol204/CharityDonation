from django.urls import path, include
from .views import LandingView

urlpatterns = [
    path('', LandingView.as_view()),
]
