from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Institution, UserProfile, Category
from django.core.paginator import Paginator
from pages.forms import UserProfilForm

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
            user_id = request.user.id
            profil = UserProfile.objects.filter(user_id=user_id)
            if profil:
                return render(request, 'home.html', context)
            else:
                return redirect('/profil/#form')
        else:
            return render(request, 'home.html', context)

class ProfilForm(View):

    def get(self, request):
        form = UserProfilForm
        context = { 'form':form}
        return render(request, 'profilForm.html', context)
    def post(self, request):
        form = UserProfilForm(request.POST)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.user = request.user
            profil.save()
            return redirect('home')


class ProfilPage(View):

    def get(self, request):
        user_id = request.user.id
        profil = UserProfile.objects.filter(user_id=user_id)
        context = {'profil': profil}
        if profil:
            return render(request, 'profil.html', context)
        else:
            return redirect('/profil/#form')


class AddDonationPage(View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', ctx)


def get_inst_by_cat(request):
    cat_id = request.GET.get('cat_id')
    if cat_id is None:
        institutions = Institution.objects.all()
    else:
        categories = Category.objects.get(pk=cat_id)
        institutions = Institution.objects.filter(category_of_items=categories)
    return render(request, 'rest_list_view.html', {'institutions': institutions})

def get_form_info(request):#

    new_array_for_stuff = []
    stuff_id_arr = request.GET.get('stuff_id_arr')
    separated_id = stuff_id_arr.split(',', )
    for stuff in separated_id:
        temporary_stuff = Category.objects.get(pk=stuff)
        new_array_for_stuff.append(temporary_stuff)

    bags_quantity = request.GET.get('bags_quantity')
    institution = request.GET.get('institution')
    street = request.GET.get('street')
    city = request.GET.get('city')
    post_code = request.GET.get('post_code')
    phone = request.GET.get('phone')
    date = request.GET.get('date')
    time = request.GET.get('time')
    comments = request.GET.get('comments')
    if comments == '':
        comments = 'Brak'
    return render(request, 'rest_form_info.html', {"bags_quantity": bags_quantity, "street": street, "city":city,
                                                   "post_code": post_code, "phone":phone, "date":date, "time":time,
                                                   "comments":comments, 'institution': institution,
                                                   "new_array_for_stuff": new_array_for_stuff})

