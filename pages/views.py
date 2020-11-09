from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Donation, Institution
# Create your views here.

class LandingView(View):

    def get(self, request):
        quantity = Donation.objects.values_list('quantity', flat=True)
        bags_of_gifts = 0
        for i in range(0,len(quantity)):
            bags_of_gifts = bags_of_gifts + quantity[i]
        all_supported_inst = len(Institution.objects.all())

        all_fund = Institution.objects.filter(type__icontains='Fundacja')

        all_org = Institution.objects.filter(type__icontains='Organizacja pozarządowoa')

        all_local_collection = Institution.objects.filter(type__icontains='Zbiórka lokalna')





        return render(request, 'home.html', {'bags_of_gifts': bags_of_gifts, 'all_supported_inst': all_supported_inst,
                                             'all_fund':all_fund, 'all_org':all_org, 'all_local_collection':all_local_collection})

