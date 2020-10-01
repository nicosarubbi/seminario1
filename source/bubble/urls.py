from django.urls import path
from bubble import views

urlpatterns = [
    path('', views.home, name='home'),
]
