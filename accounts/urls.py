from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    # built in Django auth
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            # searches for specific path & sends back to profile if success.
            template_name="registration/password_change_form.html",
            success_url=reverse_lazy("profile"),
        ),
        name="password_change",
    ),
    # custom signup
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("update-profile", views.profile_update, name="update_profile"),
]
