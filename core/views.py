from django.shortcuts import render, redirect
from .models import Note
from .form import NoteForm
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')



def view_notes(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'core/view_note.html', {'notes': notes})

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            return render(request, "core/signup.html", {"error": "Username and password required"})
        if User.objects.filter(username=username).exists():
            return render(request, "core/signup.html", {"error": "Username taken"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("home")
    return render(request, "core/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("post_login")  # intentional placeholder to fix later
        
        return render(request, "core/login.html", {"error": "Invalid credentials"})
    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_notes")
    else:
        form = NoteForm()
    return render(request, "core/add_note.html", {"form": form})

from .models import UserProfile

def dashboard(request):
    profile = request.user.profile  # ❌ unsafe – may not exist
    return render(request, "core/dashboard.html", {"profile": profile})
