from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# ---------------------------
# STUDENT REGISTRATION FORM
# ---------------------------
class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        if commit:
            user.save()
        return user


# ---------------------------
# COMPANY REGISTRATION FORM
# ---------------------------
class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(required=True)
    company_website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'company_name', 'company_website', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        user.company_name = self.cleaned_data['company_name']
        user.company_website = self.cleaned_data.get('company_website', '')
        if commit:
            user.save()
        return user


# ---------------------------
# LOGIN FORM
# ---------------------------
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


# ---------------------------
# PROFILE UPDATE FORM
# ---------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'bio', 'company_name', 'company_website']
