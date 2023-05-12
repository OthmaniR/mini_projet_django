from django.urls import path
from . import views
from .views import special_template

urlpatterns = [
    path('', views.Search_Phone, name='Search_Phone'),
]