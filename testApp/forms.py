from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from testApp.models import comment,Profile
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
#from django.contrib.auth import get_user_model
#User = get_user_model()

def validate_pass(value):
    if len(value) < 4:
        raise ValidationError('password must be contain 5 character')
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150,required=True, help_text='Email')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
    def save(self,commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.flast_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email__iexact = email)

        if query.exists():
            raise forms.ValidationError('That Email is already taken. Please choose another!')
        return email

from django.contrib.auth.hashers import check_password
from django.contrib.auth import login,authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')   
        if username and password:
            query = User.objects.filter(username__iexact = username)
            if not query.exists():
                raise forms.ValidationError('The user does not exist')
            else:
                is_active_query = User.objects.filter(username__iexact = username, is_active=True)
                if not is_active_query.exists():
                    raise forms.ValidationError('Account is not active, your need to activate your account before login. An account activation link has been sent to your mailbox')                
                else:
                    user = authenticate(username=username, password=password)  
                    if not user:
                        raise forms.ValidationError("Incorrect password. Please try again!")
        return super(UserLoginForm, self).clean(*args, **kwargs)
    


class SendEmailForm(forms.Form):
    Name = forms.CharField()
    Email = forms.EmailField()
    To = forms.EmailField()
    Comments = forms.CharField(required=False,widget=forms.Textarea())

class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('body',)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio','gender','address','DOB','website_url','facebook_url','Instagram_url']

class EditSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']