from django import forms
from .models import Note

from django.core.exceptions import ValidationError

class NoteForm(forms.ModelForm):
    class Meta:
        models = Note
        fields = ["title", "content"]

    def clean_title(self):
        t = self.cleaned_data.get("title", "").strip()
        if not t:
            raise ValidationError("Title is required.")
        return t
