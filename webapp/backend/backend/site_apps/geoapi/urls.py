from .urls import weight_search
from django.urls import path, re_path

urlpatterns = [
    path("weight", weight_search),
]