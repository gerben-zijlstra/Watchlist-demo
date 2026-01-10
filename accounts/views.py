from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm


# sending user to their respective profile,
# if they are logged in
@login_required
def profile(request):
    return render(request, "profile.html")


# function for updating profile of the linked user.
# since User and Profile are seperate, there are 2 forms which have to be updated.
#
@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account updated for {request.user.username}")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "update_profile.html", {"u_form": u_form, "p_form": p_form})


# simple signup function view with UserCreationForm
# and validation.
# on success, logs user in and saves user with hashed pass.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})
