
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO
import os
import csv
import qrcode
import re
from .models import QRCode, QRCodeData
from .forms import UserRegistrationForm, CSVUploadForm
from django.contrib.auth.decorators import login_required

# Home view function to render the home page
def home(request):
    return render(request, 'accounts/home.html')

# User registration view
def register(request):
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

# User login view
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
    return render(request, 'accounts/login.html', {'form': form})

# User logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

# User profile view
@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

# View to display all generated QR codes for the logged-in user
@login_required
def view_qr_codes(request):
    qr_codes = QRCode.objects.filter(user=request.user)
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})

# View to handle CSV uploads and generate QR codes
@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            headers = next(reader, None)  # Assuming the first row is the header

            for row in reader:
                attributes = [f"{headers[i]}: {row[i]}" for i in range(len(headers))]
                row_data = '\n'.join(attributes)

                # Create and save the QRCode object with the encoded data
                qr_code = QRCode(name=row[0], data=row_data, user=request.user)
                qr_code.save()

                # Generate a URL pointing to the display page for this QR code
                qr_code_url = f"https://www.csvtoqrcode.com/qr/{qr_code.id}/"
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(qr_code_url)
                qr.make(fit=True)

                # Save the QR code image in memory
                img_buffer = BytesIO()
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                img_name = f"{row[0]}_{row[1]}.png"
                img_content = ContentFile(img_buffer.read())
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})

# View to display QR code data
def display_qr_data(request, qr_id):
    try:
        qr_data = QRCodeData.objects.get(id=qr_id)  # Fetch data based on QR code ID
        data = qr_data.data
    except QRCodeData.DoesNotExist:
        return HttpResponse("Invalid QR code.", status=404)

    return render(request, 'accounts/display_qr_data.html', {'data': data})

# View to download all generated QR codes as a ZIP file
@login_required
def download_all_qr_codes(request):
    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        qr_codes = QRCode.objects.all()
        for qr_code in qr_codes:
            qr_path = qr_code.filename.path
            zip_file.write(qr_path, os.path.basename(qr_path))

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'
    return response

# View to download a specific QR code
@login_required
def download_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id, user=request.user)
    response = HttpResponse(qr_code.filename, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{qr_code.filename.name}"'
    return response
'''
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage
from django.urls import reverse
from django.conf import settings
from zipfile import ZipFile
from io import BytesIO
import os
import csv
import qrcode
import re
from .models import QRCode, QRCodeData
from .forms import UserRegistrationForm, CSVUploadForm
from django.contrib.auth.decorators import login_required

# Home view function to render the home page
def home(request):
    return render(request, 'accounts/home.html')

# User registration view
def register(request):
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

# User login view
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
    return render(request, 'accounts/login.html', {'form': form})

# User logout view
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

# User profile view
@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

# View to display all generated QR codes for the logged-in user
@login_required
def view_qr_codes(request):
    qr_codes = QRCode.objects.filter(user=request.user)
    return render(request, 'accounts/view_qr_codes.html', {'qr_codes': qr_codes})

# View to handle CSV uploads and generate QR codes (skipping the header row)
@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)

            headers = next(reader, None)  # Skip the first row (header)

            for row in reader:
                attributes = [f"{headers[i]}: {row[i]}" for i in range(len(headers))]
                row_data = '\n'.join(attributes)

                # Create and save the QRCode object with the encoded data
                qr_code = QRCode(name=row[0], data=row_data, user=request.user)
                qr_code.save()

                # Generate a URL pointing to the display page for this QR code
                qr_code_url = reverse('display_qr_data', args=[qr_code.id])  # Unique link for each QR code
                full_url = f"https://www.csvtoqrcode.com{qr_code_url}"  # Adjust domain as needed
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(full_url)
                qr.make(fit=True)

                # Save the QR code image in memory
                img_buffer = BytesIO()
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                img_name = f"{row[0]}_{row[1]}.png"
                img_content = ContentFile(img_buffer.read())
                qr_code.filename.save(img_name, img_content, save=True)

            messages.success(request, "CSV uploaded successfully, and QR codes were generated.")
            return redirect('view_qr_codes')
    else:
        form = CSVUploadForm()

    return render(request, 'accounts/upload_csv.html', {'form': form})

# View to display QR code data
def display_qr_data(request, qr_id):
    try:
        qr_code = QRCode.objects.get(id=qr_id)  # Fetch the data based on the QR code ID
        data = qr_code.data
    except QRCode.DoesNotExist:
        return HttpResponse("Invalid QR code.", status=404)

    return render(request, 'accounts/display_qr_data.html', {'data': data})


# View to download all generated QR codes as a ZIP file
@login_required
def download_all_qr_codes(request):
    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        qr_codes = QRCode.objects.all()
        for qr_code in qr_codes:
            qr_path = qr_code.filename.path
            zip_file.write(qr_path, os.path.basename(qr_path))

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=qr_codes.zip'
    return response

# View to download a specific QR code
@login_required
def download_qr_code(request, qr_code_id):
    qr_code = get_object_or_404(QRCode, id=qr_code_id, user=request.user)
    response = HttpResponse(qr_code.filename, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{qr_code.filename.name}"'
    return response