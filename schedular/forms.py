from django import forms
from . import models
# from mysite.movie.models import SetMovie
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(
        label = "Password",
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    password2 = forms.CharField(
    label = "Confirm Password",
    widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email',]

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            # 'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'password2': forms.PasswordInput(attrs={'class':'form-control'}),
        }


class BookedSeatForm(forms.Form):
    booked_seats = forms.IntegerField()



class CheckEligibilityForm(forms.Form):
    vaccine_dose = forms.IntegerField()
    # vaccine_certificate = forms.FileField()
    name = forms.CharField()

    