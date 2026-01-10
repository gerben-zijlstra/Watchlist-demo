from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    GENRE_CHOICES = [
        ("None", "None"),
        ("Action", "Action"),
        ("Comedy", "Comedy"),
        ("Drama", "Drama"),
        ("Sci-Fi", "Sci-Fi"),
        ("Horror", "Horror"),
        ("Documentary", "Documentary"),
    ]

    favorite_genre = forms.ChoiceField(
        choices=GENRE_CHOICES, widget=forms.Select(attrs={"class": "form-select"})
    )

    dark_mode = forms.ChoiceField(
        choices=[(False, "Light Mode"), (True, "Dark Mode")],
        widget=forms.Select(
            attrs={"class": "form-select", "placeholder": "No genres set"}
        ),
    )

    class Meta:
        model = Profile
        fields = ["image", "bio", "favorite_genre", "dark_mode"]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Tell us about your movie taste...",
                }
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_dark_mode(self):
        data = self.cleaned_data["dark_mode"]
        if data == "True" or data is True:
            return True
        return False
