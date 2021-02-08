from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Institution, UserProfile, Category
from django.core.paginator import Paginator
from pages.forms import UserProfilForm
import datetime

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
        min_date = datetime.date.today() + datetime.timedelta(days=1)
        min_date = min_date.strftime("%Y-%m-%d")
        print(min_date)
        ctx = {
            'categories': categories,
            'institutions': institutions,
            'min_date': min_date,
        }
        return render(request, 'form.html', ctx)

    def post(self, request):

        new_array_for_stuff = []
        stuff_id_arr = request.POST.get('stuff_id_arr')
        separated_id = stuff_id_arr.split(',', )
        for stuff in separated_id:
            temporary_stuff = Category.objects.get(pk=stuff)
            new_array_for_stuff.append(temporary_stuff)

        bags_quantity = request.POST.get('bags_quantity')
        inst = request.POST.get('institution')
        institution = Institution.objects.get(pk=inst)
        street = request.POST.get('street')
        city = request.POST.get('city')
        zip_code = request.POST.get('post_code')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        comments = request.POST.get('comments')
        if comments == '':
            comments = 'Brak'

        new_donation = Donation()

        new_donation.institution = institution
        new_donation.quantity = bags_quantity
        new_donation.address = street
        new_donation.phone_number = phone
        new_donation.city = city
        new_donation.pick_up_date = date
        new_donation.zip_code = zip_code
        new_donation.pick_up_time = time
        new_donation.pick_up_comment = comments
        new_donation.user = request.user
        new_donation.save()

        for i in range(len(new_array_for_stuff)):
            new_donation.categories_of_items.add(new_array_for_stuff[i])
            i += 1
        return redirect("/")

def get_inst_by_cat(request):
    cat_id = request.GET.get('cat_id')
    if cat_id is None:
        institutions = Institution.objects.all()
    else:
        categories = Category.objects.get(pk=cat_id)
        institutions = Institution.objects.filter(category_of_items=categories)
    return render(request, 'rest_list_view.html', {'institutions': institutions})

def get_form_info(request):

    new_array_for_stuff = []
    stuff_id_arr = request.GET.get('stuff_id_arr')
    separated_id = stuff_id_arr.split(',', )
    for stuff in separated_id:
        temporary_stuff = Category.objects.get(pk=stuff)
        new_array_for_stuff.append(temporary_stuff)

    bags_quantity = request.GET.get('bags_quantity')
    inst = request.GET.get('institution')
    institution = Institution.objects.get(pk=inst)
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

def form_confirmation(request):
    return render(request, 'form-confirmation.html')