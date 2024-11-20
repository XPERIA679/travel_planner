from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.itinerary_view, name='Generate Itinerary'),
]
