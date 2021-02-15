from .views import weight_search, metro_counties, all_election_precincts, get_metro_parcel_ids, get_precinct_stat_ranges
from django.urls import path, re_path

urlpatterns = [
    re_path("^counties", metro_counties),
    re_path("^weight", weight_search),
    re_path("^election/precinctstatsrange", get_precinct_stat_ranges),
    re_path("^election/precincts", all_election_precincts),
    re_path("^election/metromodel", get_metro_parcel_ids),
]