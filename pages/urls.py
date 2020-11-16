from django.urls import path, include
from .views import LandingView, ProfilView

urlpatterns = [
    path('', LandingView.as_view(), name='home'),
    path('profil/', ProfilView.as_view(), name='profil'),
]
