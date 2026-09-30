from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/company-verification/submit/', views.submit_company_verification, name='submit-company-verification'),
]
