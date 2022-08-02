from django.urls import path
from . import views


app_name = 'myBoard'

urlpatterns = [
    path('', views.index, name='index'),
]