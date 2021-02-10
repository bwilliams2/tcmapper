import pandas as pd
import pytest
from geotools.election import all_election_data

# @pytest.mark.parametrize("year",[2020, 2018, 2016, 2014, 2012])
def test_all_election_data(year):
    data, features = all_election_data(year=year)
    assert isinstance(data, pd.DataFrame)
    assert len(data) == len(features)
