from django.urls import path
from caduceus import views

urlpatterns = [
    path('', views.home, name='home'),
]
