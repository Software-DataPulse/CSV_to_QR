# accounts/urls.py

#import qr_generator_project

from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.home, name='home'),  # Home/Login page
    path('login/', views.home, name='login'),  # Login page
    path('register/', views.register, name='register'),  # Registration page
    path('profile/', views.profile, name='profile'),  # Profile page
    path('upload_qr/', views.upload_qr, name='upload_qr_page'),  # CSV Upload & QR Generation
    path('download_qr_zip/', views.download_qr_zip, name='download_qr_zip'),  # Download ZIP of QR codes
    path('logout/', views.user_logout, name='logout'),  # Log out functionality
    path('change_password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    #path('display_qr_data/<int:qr_code_id>/', views.display_qr_data, name='display_qr_data'),
]