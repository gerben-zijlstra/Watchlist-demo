from django import forms
from .models import Watchlist


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Christmas Movies"}
            ),
            "description": forms.Textarea(attrs={"class": "formcontrol", "rows": 2}),
        }
