from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('create/', views.create_opportunity, name='create_opportunity'),
]
