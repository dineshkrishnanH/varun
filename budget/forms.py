from django import forms

from budget.models import Expense

from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):

    class Meta:

        model=Expense
        
        exclude=("created_date","user")

        widget={
            "title":forms.TextInput(attrs={"class":"form-control"}),

            "amount":forms.IntegerField(),

            "category":forms.Select(attrs={"class":"form-control form-select"}),
        }

class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User
        fields=[
            "username","email","password"
        ]
        widgets = { 'username': forms.TextInput(attrs={'class': 'form-control'}),
                   
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),

                    'password': forms.PasswordInput(attrs={'class': 'form-control'}), }
        
# class SignInForm(forms.Form):

#     username=forms.CharField()

#     password=forms.CharField(widget=forms.PasswordInput())

from django import forms

class SignInForm(forms.Form):
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

