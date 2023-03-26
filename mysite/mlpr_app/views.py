from django.shortcuts import render, redirect

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
        # filename = 'heart.csv'
        file_url = settings.MEDIA_ROOT + "\\" + filename
        
        prediction = get_prediction(file_url, request.POST)
        input_data = {}
        input_data.update(request.POST)
        return render(request, 'mlpr_app/prediction.html', {
            'prediction': prediction, 'input_parameter': input_data
        })
    return render(request, 'mlpr_app/home.html', {"debug": debug})
