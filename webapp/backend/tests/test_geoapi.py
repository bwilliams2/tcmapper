from backend.site_apps.geoapi.views import weight_search
from rest_framework.test import APIRequestFactory
rf = APIRequestFactory()


def test_weight_search():
    request = rf.get("api/weight", {"longitude": -93.134160, "latitude": 45.147762, "radius": 5000})
    res = weight_search(request)
    assert len(res.data) > 0      

