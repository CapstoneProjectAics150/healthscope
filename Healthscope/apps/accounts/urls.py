from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("accounts/login/", views.user_login, name="login"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/logout/", views.user_logout, name="logout"),
    path("accounts/profile_create/", views.profile_create, name="profile_form"),
    path("accounts/profile_view/", views.profile_view, name="profile"),
    path("accounts/profile_update/", views.profile_update, name="update"),
]