from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extends the default User model to include additional fields for user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

from django.db import models
from django.contrib.auth.models import User

class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qr_codes', null=True, blank=True)
    name = models.CharField(max_length=255, help_text="The name or identifier for the QR code.")
    data = models.TextField(help_text="The data associated with the QR code.")
    filename = models.ImageField(upload_to='qr_codes/', help_text="The generated QR code image file.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class QRCodeData(models.Model):
    """
    Model to store structured data associated with QR codes.
    """
    data = models.TextField(help_text="The data associated with the QR code.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Code Data - {self.data[:50]}"  # Display first 50 characters of the data in the admin interface