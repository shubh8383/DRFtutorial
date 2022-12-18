# basic_api/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from basic_api import views

app_name="basic_api"

urlpatterns = [
    path('upload/', views.UploadFileView.as_view(), name='upload-file'),
    path('basic/', views.API_objects.as_view(), name="homepage"),
    path('basic/<int:pk>/', views.API_objects_details.as_view()),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("home/", views.Home_view, name="home"),
    path("logout/", views.logout_request, name="logout")
]

urlpatterns = format_suffix_patterns(urlpatterns)