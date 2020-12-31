from geotools.stats import growth_rates

def test_growth_rates():
    from geotools.path_calc import parcel_address_search
    lat, lng = [45.147762, -93.134160]
    address_data, features = parcel_address_search(lng, lat, 5000)
    class_rates = growth_rates(address_data)
    d = 5
