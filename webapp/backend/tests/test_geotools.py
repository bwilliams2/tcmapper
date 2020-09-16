from backend.geotools.path_calc import address_search

def test_path_calc():
    lat, lng = [45.147762, -93.134160]
    address_data = address_search(lng, lat, 5000)
    assert address_data.shape[0] > 0 and (address_data["DISTANCE"] < 5000).all()

