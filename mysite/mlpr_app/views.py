from django.shortcuts import render, redirect
from numpy import array
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
from . models import SearchLog
from .modeling import *


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
        # return redirect('/select_output/' + filename)
        return render(request, 'mlpr_app/prediction.html', {
            'uploaded_file_url': list(uploaded_file_url)
        })
    return render(request, 'mlpr_app/home.html', {"debug": debug})
