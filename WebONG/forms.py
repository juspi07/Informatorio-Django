from django import forms
from .models import *

# Create your forms here.



class Register(forms.Form):
	username = forms.CharField(label='Usuario', max_length=10, required=True)
	password = forms.CharField(label='Contraseña', max_length=10, required=True)

class Login(forms.Form):
	username = forms.CharField(label='Usuario', max_length=10, required=True)
	password = forms.CharField(label='Contraseña', max_length=10, required=True)

