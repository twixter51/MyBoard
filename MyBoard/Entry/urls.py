from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.index, name="index"),
    path("Board/", views.board, name="board"),
    path("Signup/", views.signup, name = "signup"),
    path("logout/", views.log_out_view, name = "logout"),
    path("main/", views.Main, name="Main"),
    path('upload/', views.upload_media, name='upload_media'),
    path("messages/", views.upload_text, name ="upload_text"),
    path("", views.home, name="home")
]