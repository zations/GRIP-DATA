from django.shortcuts import render, redirect
from .models import Note
from .form import NoteForm
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_notes')
    else:
        form = NoteForm()
    return render(request, 'core/add_note.html', {'form': form})

def view_notes(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'core/view_notes.html', {'notes': notes})
