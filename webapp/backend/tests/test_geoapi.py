from backend.site_apps.geoapi.views import weight_search, all_election_precincts
from rest_framework.test import APIRequestFactory
rf = APIRequestFactory()


def test_weight_search():
    request = rf.get("api/weight", {"longitude": -93.134160, "latitude": 45.147762, "radius": 5000})
    res = weight_search(request)
    assert len(res.data) > 0      

def test_all_election_precincts():
    request = rf.get("api/election")
    res = all_election_precincts(request)
    assert len(res.data) > 0

