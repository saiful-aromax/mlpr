
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('select_output/<str:file_name>/', views.select_output, name='Select Output'),
    path('evaluation_mc/<str:file_name>/<str:y>/<int:mc>/<int:split>/', views.modeling, name='Model Evaluation MC'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('dis', views.dis, name='dis')
]
