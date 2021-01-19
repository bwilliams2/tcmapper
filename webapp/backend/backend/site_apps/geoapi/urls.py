from .views import weight_search, metro_counties
from django.urls import path, re_path

urlpatterns = [
    re_path("^counties", metro_counties),
    re_path("^weight", weight_search),
]