from django.shortcuts import render
from numpy import array
# from django.http import HttpResponse
from . models import SearchLog
# from . raw_query import raw_query


# Create your views here.


def home(request):
    AroVar = {"alpha": "A", "bita": "B", "gamma": 'C'}
    return render(request, 'mlpr_app/home.html', {"AroVar": AroVar})


def about(request):
    GetInfo = SearchLog.objects.all()
    return render(request, 'mlpr_app/about.html', {"GetInfo": GetInfo})


def contact(request):
    commodities = []
    return render(request, 'mlpr_app/contact.html', {"commodities": commodities})

def dis(request):
    array_list = array(["Saiful", "Aromax", 3, 4])
    print(array_list[1])
    disaggregates = raw_query("SELECT * FROM erm.disaggregates")
    return render(request, 'mlpr_app/dis.html', {"disaggregates": disaggregates, "array_list": array_list})
