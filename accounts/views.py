from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


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
