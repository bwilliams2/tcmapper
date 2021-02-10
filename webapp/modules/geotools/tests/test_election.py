import pandas as pd
from geotools.election import all_election_data

def test_all_election_data():
    data, features = all_election_data()
    assert isinstance(data, pd.DataFrame)
    assert len(data) == len(features)
