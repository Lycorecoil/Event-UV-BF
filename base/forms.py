from django.forms import ModelForm
from .models import Event
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class EvenForm(ModelForm):
	date = forms.DateTimeField(
		widget= forms.DateInput(
			attrs={
				'class': 'form-control',
				'type':'datetime-local'
			},
			
		)

	)
	class Meta:
		model = Event
		fields ='__all__'
		exclude=['host', 'participants']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','email']
		

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InviteForm(forms.Form):
	name=forms.CharField(max_length=64)
	mail = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)

