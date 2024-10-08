# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import QRCode

class UserRegistrationForm(forms.ModelForm):
    """
    A form for registering new users. Includes all the required
    fields, plus a repeated password for verification.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password_confirm(self):
        # Ensure the passwords match
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm

class CSVUploadForm(forms.Form):
    """
    A form for uploading a CSV file. The CSV is used to generate QR codes.
    """
    csv_file = forms.FileField()