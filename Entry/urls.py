from django.urls import path
from . import views
from .models import users, userMedia, userTexts

urlpatterns = [
    path("login/", views.index, name="index"),
    path("signup/", views.signup, name = "signup"),
    path("logout/", views.log_out_view, name = "logout"),
    path("choice/", views.choice_view, name="choice"),
    path("premium_sale/",  views.premium_sale, name="premium_sale"),

    #payment
    path("checkout/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.checkout_success, name="checkout_success"),
    path("cancel/", views.checkout_cancel, name="checkout_cancel"),
    
    # change main path based on uniLink?
    path("board/<slug:boardLink>", views.Main, name="Main"),
    path("guest/start/", views.create_guest, name="create_guest"),

    path('upload/', views.upload_media, name='upload_media'),
    path("messages/", views.upload_text, name ="upload_text"),
    path("delete/", views.remove_content, name = "remove_content"),
    path("update_user/", views.update_user, name="update_user"),
    path("", views.home, name="home")
]

