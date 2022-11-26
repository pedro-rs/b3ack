from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.cache import never_cache

import json

from b3ack.utils.b3api import B3api
from b3ack.utils.bcolors import bcolors
from b3ack.utils.tracking import Tracking

# Models
from .models import InvestorUser, CompanyTracker

# Needed since using 
from django.contrib.auth import get_user_model
User = get_user_model()

def index_view(request):
    return render(request, "b3ack/index.html", {
        "message": "As senhas devem ser iguais."
    })


def login_view(request):
    cache.clear()

    if request.method == "POST":
        # Attempt to authenticate user
        username = request.POST["username"]
        password = request.POST["password"]

        redirect = request.session['redirect']
        redirect_code = request.session['redirect_code']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Authentication successful
            login(request, user)

            if redirect is not None:
                return HttpResponseRedirect(reverse(redirect, args=(redirect_code,)))
            else:
                return HttpResponseRedirect(reverse("index"))

        else:
            # Authentication failed
            return render(request, "b3ack/login.html", {
                "message": "Credenciais incorretas!"
            })

    else:
        if not request.user.is_authenticated:
            redirect = request.GET.get('redirect')
            code = request.GET.get('code')

            request.session['redirect'] = redirect
            request.session['redirect_code'] = code

            return render(request, "b3ack/login.html")
        else:
            return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    cache.clear()
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    cache.clear()

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "b3ack/register.html", {
                "message": "As senhas devem ser iguais."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            return render(request, "b3ack/register.html", {
                "message": "Email ou nome de usuário indisponível."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        if not request.user.is_authenticated:
            return render(request, "b3ack/register.html")
        else:
            return HttpResponseRedirect(reverse("index"))

@cache_page(300)
def search_view(request):
    api = B3api()

    return render(request, "b3ack/search.html", {
        "data": api.data.values()
    })

@never_cache
@cache_page(300)
def company_view(request, code):
    api = B3api()
    company = api.data[code]
    quotes = api.get_quotes(code=code)

    if request.user.is_authenticated and len(request.user.watchlist.filter(code=code)) != 0:
        # User currently has this company os his watchlist
        # Therefore, display graph os tracked stock data
        data = dict()

        company_data = request.user.watchlist.filter(code=code)[0]
        data['labels'] = company_data.capture_dt
        data['values'] = company_data.abr

    else:
        data = None

    relevant_quote = list(quotes.values())[0]

    return render(request, "b3ack/company.html", {
        "company": company,
        "quotes": relevant_quote,
        "data": data
    })

@csrf_exempt
@login_required
def watchlist_view(request):
    if request.method == "POST":
        cache.clear()

        data = json.loads(request.body)

        # Fetching form data
        company_code = data['companyCode']
        interval = int(data['interval']) * 60 # Converted to minutes
        buy_value = float(data['buy_value'])
        sell_value = float(data['sell_value'])

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
        return HttpResponseRedirect(reverse("profile"))

@login_required()
def profile_view(request):
    active_trackers = request.user.tracks.all()
    print(active_trackers)
    return render(request, "b3ack/profile.html", {
        "active_trackers": active_trackers,
    })
