from rest_framework import routers
from django.urls import path, include
from .api import get_level


urlpatterns = [
    path('level/', get_level),
]