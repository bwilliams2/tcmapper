import pandas as pd
import pytest
from geotools.election import all_election_data, metro_ids, precinct_stat_ranges, model_nearest_neighbors

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

def test_model_nearest_neighbors():
    inputs = {
        "cit_dis": 16,
        "mean_emv": 200000,
        "growth": 0.01,
        "mean_age": 1999,
        "usprs_vote_density": 1 * 10 ** 6
    }
    closest_ids = model_nearest_neighbors(10, **inputs)
    assert len(closest_ids) == 10