from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password1','password2')

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('The entered password already exist')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('The entered email already exist')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return p2

    def save(self,commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data['password1'])
       if commit:
           user.save()
       return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='Click on <a href=\'../password\'>this link</a> for change password')

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password','is_active','is_admin','last_login')


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField()
    email = forms.CharField()
    full_name = forms.CharField()
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm_Password',widget=forms.PasswordInput)


    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return p2

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('The entered phone number already exist')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('The entered email already exist')
        return email


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)



