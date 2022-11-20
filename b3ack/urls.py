from django.urls import path
from . import views
from b3ack.utils.tracking import Tracking


urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search_view, name="search"),
    path("company/<str:cod>", views.company_view, name="company"),

    path("watchlist", views.watchlist_view, name="watchlist"),
]

# Whenever app starts, start tracking quotes
Tracking(60).start_tracking()