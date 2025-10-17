from django.urls import path
from . import views 

urlpatterns = [
   path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("add/", views.add_note, name="add_note"),
    path("notes/", views.view_notes, name="view_notes"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="accounts_login"),
    path("logout/", views.logout_view, name="logout"),
    path("post-login/", views.view_notes, name="post_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("note_list/", views.note_list, name="note_list"),
    path("note_detail/", views.note_detail, name="note_detail"),


    
]