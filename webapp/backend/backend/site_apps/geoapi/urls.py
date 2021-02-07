from .views import weight_search, metro_counties, all_election_precincts
from django.urls import path, re_path

urlpatterns = [
    re_path("^counties", metro_counties),
    re_path("^weight", weight_search),
    re_path("^election/metroprecincts", all_election_precincts)
]