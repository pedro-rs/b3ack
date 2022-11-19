from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("company/<str:cod>", views.company, name="company"),
    # path("<str:name>", views.greet, name="greet")
]