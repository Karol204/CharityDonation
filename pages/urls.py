from django.urls import path, include
from .views import LandingView, ProfilForm, ProfilPage

urlpatterns = [
    path('', LandingView.as_view(), name='home'),
    path('profil/', ProfilForm.as_view(), name='profil'),
    path('profilView/', ProfilPage.as_view(), name='profilpage'),
]
