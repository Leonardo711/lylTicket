#-*-coding:utf-8-*-
from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.EmailField(label="邮箱")
    password = forms.CharField(label = "密码", widget=forms.PasswordInput)
    passwordagain = forms.CharField(label = "确认密码", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordagain')
        if password1 and password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

class SignInForm(forms.Form):
    username = forms.EmailField(label="邮箱")
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    username = forms.EmailField(label="邮箱")
#   password = forms.CharField(label = "密码", widget=forms.PasswordInput)
#   passwordagain = forms.CharField(label = "确认密码", widget=forms.PasswordInput)


class PasswordResetForm2(forms.Form):
#   username = forms.EmailField(label="邮箱")
    password = forms.CharField(label = "密码", widget=forms.PasswordInput)
    passwordagain = forms.CharField(label = "确认密码", widget=forms.PasswordInput)

class PasswordChangeForm(forms.Form):
    originalpassword = forms.CharField(label = "原密码", widget=forms.PasswordInput)
    password = forms.CharField(label = "密码", widget=forms.PasswordInput)
    passwordagain = forms.CharField(label = "确认密码", widget=forms.PasswordInput)