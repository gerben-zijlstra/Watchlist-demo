from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # built in login/logout
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # custom signup
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
]
