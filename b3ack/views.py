from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import json
import ast

from b3ack.utils.b3api import B3api
from b3ack.utils.bcolors import bcolors
from b3ack.utils.tracking import Tracking

# Models
from .models import InvestorUser, CompanyTracker

# Needed since using 
from django.contrib.auth import get_user_model
User = get_user_model()

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

    if request.user.is_authenticated and len(request.user.watchlist.filter(code=cod)) != 0:
        # User currently has this company os his watchlist
        # Therefore, display graph os tracked stock data
        data = dict()

        company_data = request.user.watchlist.filter(code=cod)[0]
        data['labels'] = company_data.capture_dt
        data['values'] = company_data.abr

        print("aqui")
        print(data)

    else:
        data = None

    return render(request, "b3ack/company.html", {
        "company": company,
        "quotes": quotes,
        "data": data
    })

@csrf_exempt
@login_required
def watchlist_view(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Fetching form data
        company_code = data['companyCode']
        interval = int(data['interval']) * 60 # Converted to minutes
        buy_value = int(data['buy_value'])
        sell_value = int(data['sell_value'])

        # Create a CompanyTracker for the user
        api = B3api()
        data = api.data[company_code]

        tracker = CompanyTracker(
            api_id     = data['id'],
            code       = data['cd_acao_rdz'],
            name       = data['nm_empresa'],
            user       = request.user,
            interval   = interval,
            buy_value  = buy_value,
            sell_value = sell_value
        )

        tracker.save()

        # Fetching user
        user_id = request.user.id
        user = InvestorUser.objects.get(id=user_id)

        # Adding Company to user's watchlist
        tracker = CompanyTracker.objects.filter(code=data['cd_acao_rdz'], user=request.user)[0]
        user.watchlist.add(tracker)

        
        print(bcolors.WARNING + f"Tracking {tracker.code} every {tracker.interval / 60} minutes for {tracker.user}!" + bcolors.ENDC)
        Tracking().start_tracking(tracker.interval, tracker.code, tracker.id)

        return JsonResponse({"message": "Added to watchlist successfully."}, status=201)

    else:
        return HttpResponseRedirect(reverse("index"))