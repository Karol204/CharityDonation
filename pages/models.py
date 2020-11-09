from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=126)

    def __str__(self):
        return f'{self.name}'

class Institution(models.Model):
    class Types(models.TextChoices):
        FUND = 'Fundacja'
        ORG = 'Organizacja pozarządowoa'
        ZBL = 'Zbiórka lokalna'

    name = models.CharField(max_length=250)
    description = models.CharField(max_length=440)
    type = models.CharField(max_length=26, choices=Types.choices, default=Types.FUND)
    category_of_items = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.name} - {self.type}'


class Donation(models.Model):
    quantity = models.IntegerField()
    categories_of_items = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=126)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=55)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.pick_up_date}'
