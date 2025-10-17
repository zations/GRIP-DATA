from django.shortcuts import render, redirect
from .models import Note
from .form import NoteForm
from django.http import HttpResponse

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

from django.db.models import Q
from django.core.paginator import Paginator

def note_list(request):
    q = request.GET.get("q", "")
    if q:
        # queryset = Note.objects.filter(
        #     Q(title__icontains=q) | Q(content__icontains=q) | Q(tag__icontains=q)
        # )
        queryset = Note.objects.search(q)

    else:
        queryset = Note.objects.all()

    paginator = Paginator(queryset, 5)  # 5 notes per page
    page = request.GET.get("page")
    notes = paginator.get_page(page)

    return render("core/note_list.html", {"notes": notes, "query": q})


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

@login_required
def dashboard(request):
    profile, _created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "core/dashboard.html", {"bio": profile.bio})
