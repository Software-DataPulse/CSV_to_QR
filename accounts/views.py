from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, CSVUploadForm
from .models import QRCode
import qrcode

# accounts/views.py

from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the email from the form
        password = request.POST.get('password')  # Get the password from the form
        user = authenticate(request, username=email, password=password)  # Authenticate user
        if user is not None:
            login(request, user)  # Log the user in
            return redirect('profile')  # Redirect to profile page after successful login
        else:
            messages.error(request, 'Invalid email or password')  # Show an error message
    return render(request, 'accounts/home.html')  # Render the home page with the login form


'''def home(request):
    """
    Home view function to render the home page.
    """
    return render(request, 'accounts/home.html')
'''

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=full_name)
                user.save()
                login(request, user)
                return redirect('profile')  # Redirect to profile after successful registration
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'accounts/register.html')  # Render registration page


'''def register(request):
    """
    View to handle user registration.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})
'''
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/home.html', {'form': form})

from django.contrib import messages
from django.shortcuts import redirect

# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')  # Render the profile page for logged-in users

'''def profile(request):
    """
    View to display the user's profile information.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})
    '''

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


# views.py
import os
import qrcode
from django.core.files.base import ContentFile
import csv

import qrcode
from django.core.files.base import ContentFile
import csv
from io import BytesIO
from django.contrib.auth.decorators import login_required

import csv
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import QRCode
from django.conf.urls.static import static

import qrcode
from django.core.files.storage import default_storage
from django.http import HttpResponse, FileResponse
from zipfile import ZipFile
import os


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')  # Redirect to profile after successful password change


import qrcode
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from zipfile import ZipFile
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import csv
import qrcode
import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import csv
import qrcode
import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import csv
import qrcode
import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
#from models import QRCodeData
from django.urls import reverse


import csv
import qrcode
import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile
from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def upload_qr(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        file_path = default_storage.save(f'temp/{csv_file.name}', ContentFile(csv_file.read()))
        absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)

        qr_codes = []
        try:
            # Open the uploaded CSV file
            with open(absolute_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:  # Ensure there are at least two columns
                        col1 = row[0].strip()
                        col2 = row[1].strip()

                        # Create a safe filename using the first two columns
                        filename_base = f"{col1}_{col2}"
                        safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', filename_base)  # Replace non-alphanumeric characters
                        truncated_filename = safe_filename[:50]  # Limit the filename length to 50 characters

                        # Generate the QR code and save it
                        qr_data = ','.join(row)  # You can customize this if you want to use specific columns for the QR content
                        qr = qrcode.make(qr_data)
                        qr_path = f'temp/{truncated_filename}.png'
                        qr_save_path = os.path.join(settings.MEDIA_ROOT, qr_path)
                        qr.save(qr_save_path)

                        # Append the QR code details for the template
                        qr_codes.append({
                            'name': truncated_filename,  # Display name of the QR code
                            'url': f'/media/temp/{truncated_filename}.png'  # URL for the QR code image
                        })

            # Prepare ZIP for download
            zip_filename = 'qr_codes.zip'
            zip_path = os.path.join(settings.MEDIA_ROOT, f'temp/{zip_filename}')
            with ZipFile(zip_path, 'w') as zip_file:
                for qr_code in qr_codes:
                    zip_file.write(os.path.join(settings.MEDIA_ROOT, f'temp/{qr_code["name"]}.png'))

            # Render the page with generated QR codes
            return render(request, 'accounts/upload_qr.html', {'qr_codes': qr_codes, 'zip_file': zip_filename})

        finally:
            os.remove(absolute_path)

    return render(request, 'accounts/upload_qr.html')

def download_qr_zip(request):
    zip_filename = request.GET.get('zip_file')
    zip_path = os.path.join(settings.MEDIA_ROOT, f'temp/{zip_filename}')
    return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename=zip_filename)



''''@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Extract the header row to use as titles
            headers = next(reader, None)  # Assuming the first row is the header

            for row in reader:
                attributes = [f"{headers[i]}: {row[i]}" for i in range(len(headers))]
                row_data = '\n'.join(attributes)

                # Create and save the QRCode object with the encoded data
                qr_code = QRCode(name=row[0], data=row_data, user=request.user)
                qr_code.save()

                # Generate a URL pointing to the display page for this QR code
                # In your views.py where you generate the QR code
                qr_code_url = f"https://www.csvtoqrcode.com/display_qr_data/{qr_code.id}/"
                # Generate the QR code with the URL
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4
                )
                qr.add_data(qr_code_url)
                qr.make(fit=True)

                # Create an image from the QRCode object
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the image to an in-memory buffer
                img_buffer = BytesIO()
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)  # Rewind the buffer to the beginning

                # Save the QR code image in the database
                img_name = f"{row[0]}_{row[1]}.png"  # Use the first and second columns for naming
                img_content = ContentFile(img_buffer.read())
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})
'''
'''
@login_required
def upload_csv(request):
    """
    View to handle CSV uploads and generate QR codes.
    The uploaded CSV is parsed, and for each row, a QR code is generated and saved.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Reading the CSV file
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            # Skip the header row
            next(reader, None)

            for row in reader:
                # Assuming that the first column in each row is the identifier/name
                name = row[0]

                # Generate the QR code
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(name)
                qr.make(fit=True)

                # Create an image from the QRCode object
                img = qr.make_image(fill_color="black", back_color="white")

                # Save the QR code image in memory
                img_name = f"{name}.png"
                img_content = ContentFile(img.tobytes())

                # Save the QR code image in the database
                qr_code = QRCode(name=name)
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})
'''
# views.py
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import default_storage
import zipfile

# views.py
# views.py
from django.contrib.auth.decorators import login_required

@login_required
def view_qr_codes(request):
    """
    View to display all the generated QR codes for the logged-in user.
    """
    # Get only the QR codes generated by the logged-in user
    qr_codes = QRCode.objects.filter(user=request.user)
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})


'''
def view_qr_codes(request):
    """
    View to display all the generated QR codes.
    Allows the user to see individual QR codes and download them all as a ZIP file.
    """
    # Get all the QR codes from the database
    qr_codes = QRCode.objects.all()
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})
'''
# views.py
import io
@login_required
def download_all_qr_codes(request):
    """
    View to download all generated QR codes as a ZIP file.
    Creates a ZIP file containing all QR code images in the database.
    """
    # Create an in-memory file
    buffer = io.BytesIO()

    # Create a zip file in the buffer
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Get all QR codes from the database
        qr_codes = QRCode.objects.all()
        for qr_code in qr_codes:
            # Get the file path of each QR code
            qr_path = qr_code.filename.path
            # Add the QR code to the zip file
            zip_file.write(qr_path, os.path.basename(qr_path))

    buffer.seek(0)

    # Create the response to download the ZIP file
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'

    return response

# accounts/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QRCode

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import QRCode
@login_required
def download_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id, user=request.user)
    response = HttpResponse(qr_code.filename, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{qr_code.filename.name}"'
    return response

from django.shortcuts import render, get_object_or_404
from .models import QRCode

from django.shortcuts import render, get_object_or_404
from .models import QRCode

from django.shortcuts import render, get_object_or_404
from .models import QRCode
'''
from django.shortcuts import render, get_object_or_404
from .models import QRCodeData

def display_qr_data(request, qr_code_id):
    qr_data = get_object_or_404(QRCodeData, id=qr_code_id)
    return render(request, 'accounts/display_qr_data.html', {'data': qr_data.data})
'''