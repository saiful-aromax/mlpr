from django.shortcuts import render, redirect
from numpy import array
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
from . models import SearchLog
from .evaluation_mc import *


debug = ""
# from . raw_query import raw_query


# Create your views here.


# def home(request):
#     AroVar = {"alpha": "A", "bita": "B", "gamma": 'C'}
#     return render(request, 'mlpr_app/home.html', {"AroVar": AroVar})

def home(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return redirect('/select_output/' + filename)
        # return render(request, 'mlpr_app/select_input.html', {
        #     'uploaded_file_url': list(uploaded_file_url)
        # })
    return render(request, 'mlpr_app/home.html', {"debug": debug})

def select_output(request, file_name):
    if request.method == 'POST':
        return redirect('/modeling/' + file_name + '/' + request.POST['data_output'] + '/' + request.POST['mc'] + '/' + request.POST['split'])
    file_url = settings.MEDIA_ROOT + "\\" + file_name
    columns = get_columns(file_url)
    return render(request, 'mlpr_app/select_output.html', {"columns": columns})

def evaluation_mc(request, file_name, y, mc, split):
    file_url = settings.MEDIA_ROOT + "\\" + file_name
    # data = data_prep(file_url, y)
    return render(request, 'mlpr_app/evaluation_mc.html')

def modeling(request, file_name, y, k, mc):
    file_url = settings.MEDIA_ROOT + "\\" + file_name
    data = data_prep(file_url, y)
    return render(request, 'mlpr_app/modeling.html')


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
