from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Donation, Institution, UserProfile, Category
from pages.forms import UserProfilForm
import datetime

# Create your views here.

class LandingView(View):

    def get(self, request):
        
        # Counter of all received gifts
        quantity = Donation.objects.values_list('quantity', flat=True)
        bags_of_gifts = 0
        for i in range(0, len(quantity)):
            bags_of_gifts = bags_of_gifts + quantity[i]

        # Number of supported institution
        all_supported_institution = len(Institution.objects.all())

        all_fund = Institution.objects.filter(type__icontains='Fundacja')
        all_org = Institution.objects.filter(type__icontains='Organizacja pozarządowoa')
        all_local_collection = Institution.objects.filter(type__icontains='Zbiórka lokalna')

        context = {
            'bags_of_gifts': bags_of_gifts,
            'all_supported_inst': all_supported_institution,
            'fund_page': all_fund,
            'org_page': all_org,
            'all_local_collection': all_local_collection
        }

        # Checking if user filled profile form
        if request.user.is_authenticated:
            user_id = request.user.id
            profile = UserProfile.objects.filter(user_id=user_id)
            if profile:
                return render(request, 'home.html', context)
            else:
                return redirect('/profil/#form')
        else:
            return render(request, 'home.html', context)




class ProfilForm(LoginRequiredMixin, View):

    def get(self, request):
        form = UserProfilForm
        context = {'form': form}
        return render(request, 'profilForm.html', context)

    def post(self, request):
        form = UserProfilForm(request.POST)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.user = request.user
            profil.save()
            return redirect('home')


class ProfilPage(LoginRequiredMixin, View):

    def get(self, request):
        user_id = request.user.id
        profil = UserProfile.objects.filter(user_id=user_id)
        user_donations = Donation.objects.filter(user=user_id)
        ctx = {
            'profil': profil,
            'user_donations': user_donations,
        }
        if profil:
            return render(request, 'profil.html', ctx)
        else:
            return redirect('/profil/#form')


class AddDonationPage(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        # Generate the earliest date for the form and pass it to widget in HTML
        min_date = datetime.date.today() + datetime.timedelta(days=1)
        min_date = min_date.strftime("%Y-%m-%d")
        ctx = {
            'categories': categories,
            'institutions': institutions,
            'min_date': min_date,
        }
        return render(request, 'form.html', ctx)


    def post(self, request):

        # Get data from form
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


        try:
            # Create new Donation object and add data to it
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
            ctx = {
                'error': False,
                'errorMessage': 'Successfully added'
            }
            return JsonResponse(ctx, safe=False)
        except:
            ctx = {
                'error': True,
                'errorMessage': 'Fail'
            }
            return JsonResponse(ctx, safe=False)



@login_required()
def get_inst_by_cat(request):
    # Function for dynamic list of institution loaded in form
    cat_id = request.GET.get('cat_id')
    if cat_id is None:
        institutions = Institution.objects.all()
    else:
        categories = Category.objects.get(pk=cat_id)
        institutions = Institution.objects.filter(category_of_items=categories)
    return render(request, 'rest_list_view.html', {'institutions': institutions})

@login_required()
def get_form_info(request):
    # Loaded data passed by user in form and pass it to confirmation page
    new_array_for_stuff = []
    # Creating array for all category of items
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

@login_required()
def form_confirmation(request):
    return render(request, 'form-confirmation.html')


def contact_form(request):

    if request.method == 'POST':
        subject = 'E-mail'
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        message = request.POST.get('message')

        mail = f'Od: {name} {surname} \n {message}  '

        try:
            send_mail(subject, mail, email, ['admin@email.com'])
        except BadHeaderError:
            return HttpResponse('invalid header found')
        return redirect('/')
