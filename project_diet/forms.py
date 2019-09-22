from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Cat, Food



def validate_new_user_username(value):
    if User.objects.filter(username=value):
        raise ValidationError("użytkownik istnieje w bazie")

class AddUserForm(forms.Form):
    name = forms.CharField(max_length=64, validators=[validate_new_user_username])
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")


class LoginForm(forms.Form):
    name = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class AddCatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}

    def clean(self):
        diet = self.cleaned_data.get('diet')

        if diet and not self.cleaned_data.get('diet_description'):
            raise ValidationError('Opisz dietę')

        return self.cleaned_data


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ["cat"]


class AddCompositionForm(forms.Form):
    name = forms.CharField(max_length=64)
    quantity = forms.IntegerField()

