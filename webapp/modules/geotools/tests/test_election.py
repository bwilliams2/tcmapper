import pandas as pd
import pytest
from geotools.election import all_election_data, metro_ids, precinct_stat_ranges

# @pytest.mark.parametrize("year",[2020, 2018, 2016, 2014, 2012])
def test_all_election_data():
    data, features = all_election_data(year=2018)
    assert isinstance(data, pd.DataFrame)
    assert len(data) == len(features)


def test_metro_ids():
    ids = metro_ids(2020)
    # Need some better test here
    assert len(ids) > 0


def test_metro_ids_closest_match():
    ids = metro_ids(2020, 180000, 1990, 10)
    # Need some better test here
    assert len(ids) > 0

def test_precinct_stat_ranges():
    ranges = precinct_stat_ranges()
    # Need some better test here
    assert len(ranges) == 3