from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from b3ack.utils.b3api import B3api
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.
def index_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Você não está logado!")
    else:
        return HttpResponse(f"Logado como {request.user}")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "b3ack/login.html", {
                "message": "Credenciais incorretas!"
            })

    else:
        return render(request, "b3ack/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "b3ack/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "b3ack/register.html", {
                "message": "Email address or username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "b3ack/register.html")


def search_view(request):
    api = B3api()

    return render(request, "b3ack/search.html", {
        "data": api.data.values()
    })

def company_view(request, cod):
    api = B3api()
    company = api.data[cod]
    quotes = api.get_quotes(cod=cod)

    return render(request, "b3ack/company.html", {
        "company": company,
        "quotes": quotes
    })