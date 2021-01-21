from geotools.path_calc import parcel_address_search, shp_parcel_address_search, shp_address_search, get_metro_bounds, parcel_address_search

def test_address_search():
    lat, lng = [45.147762, -93.134160]
    address_data, features = shp_address_search(lng, lat, 5000)
    assert address_data.shape[0] > 0 and (address_data["DISTANCE"] < 5000).all()

def test_postgis_address_search():
    lat, lng = [45.147762, -93.134160]
    address_data, features = parcel_address_search(lng, lat, 5000)
    assert address_data.shape[0] > 0 and (address_data["DISTANCE"] < 5000).all()

def test_shp_parcel_address_search():
    lat, lng = [45.147762, -93.134160]
    address_data, features = shp_parcel_address_search(lng, lat, 5000)
    assert address_data.shape[0] > 0 and (address_data["DISTANCE"] < 5000).all()

def test_get_metro_bounds():
    bounds = get_metro_bounds()
    


