from django.urls import path
from . import views

urlpatterns = [
    path('', views.trending_map, name='trending.map'),
]