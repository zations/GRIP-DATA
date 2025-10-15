from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    title = forms.CharField(required=False)  # BUG: allow blank

    class Meta:
        model = Note
        fields = ["title", "content"]

