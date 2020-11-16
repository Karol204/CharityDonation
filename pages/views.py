
from django.contrib.auth import get_user_model
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Donation, Institution, UserProfile
from django.core.paginator import Paginator
from pages.forms import UserProfilForm
from django.contrib.auth import get_user_model
# Create your views here.

class LandingView(View):

    def get(self, request):

        quantity = Donation.objects.values_list('quantity', flat=True)
        bags_of_gifts = 0
        for i in range(0, len(quantity)):
            bags_of_gifts = bags_of_gifts + quantity[i]
        all_supported_inst = len(Institution.objects.all())

        # <-------- Paginacja fundacji ------->
        all_fund = Institution.objects.filter(type__icontains='Fundacja')
        fund_paginator = Paginator(all_fund, 1)

        fund_page = fund_paginator.get_page(1)

        # <-------- Paginacja organizacji ------>
        all_org = Institution.objects.filter(type__icontains='Organizacja pozarządowoa')

        org_paginator = Paginator(all_org, 1)

        org_page_num = request.GET.get('org_page')
        org_page = org_paginator.get_page(1)

        all_local_collection = Institution.objects.filter(type__icontains='Zbiórka lokalna')

        context = {
            'bags_of_gifts': bags_of_gifts,
            'all_supported_inst': all_supported_inst,
            'fund_page': fund_page,
            'org_page': org_page,
            'all_local_collection': all_local_collection
        }

        if request.user.is_authenticated:
            user_name = request.user.first_name
            if user_name != "":
                return render(request, 'home.html', context)
            else:
                return redirect('/profil/#form')
        else:
            return render(request, 'home.html', context)

class ProfilView(View):

    def get(self, request):
        form = UserProfilForm
        context = { 'form':form}
        return render(request, 'profil.html', context)
    def post(self, request):
        form = UserProfilForm(request.POST)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.user = request.user
            profil.save()
            return redirect('home')


