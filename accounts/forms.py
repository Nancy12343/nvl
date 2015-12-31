__author__ = 'tq'
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AccountForm(forms.Form):

    username = forms.CharField(required=True, max_length=100, label='Username')
    password = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput, label='Password')


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)

        if self.user is None:
            msg = 'Invalid Username and / or Password'
            raise forms.ValidationError(msg)
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        return authenticate(username=username, password=password)


class RegisterForm(forms.Form):
    nickname = forms.CharField(max_length=100, label='Nickname')
    username = forms.CharField(required=True, max_length=100, label='Username')
    password = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput, label='Password')
    confirm_pwd = forms.CharField(required=True, max_length=20, widget=forms.PasswordInput, label='Confirm Password')
    email = forms.EmailField(required=True,label='Email',
                    error_messages={'invalid': 'Please enter a valid Email',
                                    'required': 'Email must not be empty'})

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_pwd = self.cleaned_data.get('confirm_pwd')

        if confirm_pwd != password:
            msg = 'Please check your Confirm Password'
            raise forms.ValidationError(msg)
        return self.cleaned_data
