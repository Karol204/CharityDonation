from django import forms
from .models import UserProfile


class UserProfilForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets =  {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'})
        }
