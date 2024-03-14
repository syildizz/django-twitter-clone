from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]

class RatingForm(forms.Form):
    CHOICES = (
        ("none", "None"),
        ("like", "👍"),
        ("dislike", "👎")
    )
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)