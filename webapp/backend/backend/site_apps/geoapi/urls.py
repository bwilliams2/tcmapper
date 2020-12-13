from .views import weight_search
from django.urls import path, re_path

urlpatterns = [
    re_path("^weight", weight_search),
]