from django.shortcuts import render
from django.http import HttpResponse
from b3ack.utils.b3api import B3api

# Create your views here.
def index(request):
    return HttpResponse("Hello World")

def search(request):
    api = B3api()
    # quotes = api.get_quotes(id=1)
    print(api.data)

    return render(request, "b3ack/search.html", {
        "data": api.data.values()
    })

def company(request, cod):
    api = B3api()
    company = api.data[cod]

    return render(request, "b3ack/company.html", {
        "company": company
    })


def greet(request, name: str):
    return render(request, "b3ack/greet.html", {
        "name": name.capitalize()
    })