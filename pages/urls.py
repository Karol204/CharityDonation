from django.urls import path, include
from .views import LandingView, ProfilForm, ProfilPage, AddDonationPage
from pages import views

urlpatterns = [
    path('', LandingView.as_view(), name='home'),
    path('profil/', ProfilForm.as_view(), name='profil'),
    path('profilView/', ProfilPage.as_view(), name='profilpage'),
    path('addDonation/', AddDonationPage.as_view()),
    path('rest/get_inst/', views.get_inst_by_cat),
    path('rest/form_info/', views.get_form_info),
    path('formConformation/', views.form_confirmation),

]
