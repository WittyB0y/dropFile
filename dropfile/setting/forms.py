from django import forms
from django.contrib.auth.models import User
from user.models import photo as Photo

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class EditUserPhoto(forms.Form):
    image = forms.ImageField()