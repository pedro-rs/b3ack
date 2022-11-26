from django.urls import path
from . import views


urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search_view, name="search"),
    path("profile", views.profile_view, name="profile"),
    path("company/<str:code>", views.company_view, name="company"),

    # API routes
    path("watchlist", views.watchlist_view, name="watchlist"),
]