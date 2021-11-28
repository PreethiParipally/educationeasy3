from django import forms
from . import models
# from mysite.movie.models import SetMovie
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class BookedSeatForm(forms.Form):
    booked_seats = forms.IntegerField()



class CheckEligibilityForm(forms.Form):
    vaccine_dose = forms.IntegerField()
    # vaccine_certificate = forms.FileField()
    name = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(CheckEligibilityForm, self).__init__(*args, **kwargs)
        self.fields['vaccine_dose'].label = "vaccine dose level taken"

        self.fields['vaccine_dose'].widget.attrs.update(
            {
                'placeholder': '0 / 1 / 2',
            }
        )
    class Meta:
        model=models.UserBook
        error_messages = {
                'vaccine_dose': {
                    'validators': 'Provide appropriate number',
                }
            }


    