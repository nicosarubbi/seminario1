from django.urls import path
from bubble import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),

    path('estudios', views.document_list, name='document-list'),
    path('estudios/alta', views.document_create, name='document-create'),
    path('estudios/<int:pk>', views.document_view, name='document-view'),
    path('estudios/<int:pk>/delete', views.document_delete, name='document-delete'),
    path('estudios/file', views.document_file, name='document-file'),

    path('vacunas', views.vaccine_list, name='vaccine-list'),
    path('vacunas/alta', views.vaccine_create, name='vaccine-create'),
    path('vacunas/<int:pk>', views.vaccine_view, name='vaccine-view'),

    path('grupo', views.group_list, name='group-list'),
    path('grupo/alta', views.group_create, name='group-create'),
    path('grupo/<int:pk>', views.group_view, name='group-view'),
]
