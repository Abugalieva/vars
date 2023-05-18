from django.forms import Form, ModelForm
from django import forms
from django.contrib.auth.models import User
from user.models import Profile


class LoginForm(Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Enter your username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                'placeholder': 'Enter your password'}))


class UserRegistrationForm(ModelForm):
    repeat_password = forms.CharField(min_length=8, max_length=20, required=True, widget=
                        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'}))

    def clean_repeat_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("repeat_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(ModelForm):
    image = forms.ImageField(required=False)
    resume = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Upload your resume here...'}))

    class Meta:
        model = Profile
        fields = ['bio', 'image', 'resume']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type something about yourself...'}),
        }
