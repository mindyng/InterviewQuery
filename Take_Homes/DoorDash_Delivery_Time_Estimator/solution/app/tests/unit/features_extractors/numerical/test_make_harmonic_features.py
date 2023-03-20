import numpy as np
import pytest

from app.features_extractors.numerical import make_harmonic_features


def test_return_pair():
    features = make_harmonic_features(np.array([]), 1)
    assert type(features) == tuple
    assert len(features) == 2


def test_value_empty():
    cos, sin = make_harmonic_features(np.array([]), 1)
    assert len(cos) == 0
    assert len(sin) == 0


def test_proper_cos():
    cos, sin = make_harmonic_features(np.array([0, 0.25, 0.5, 0.75, 1]), 1)
    for i, expected in enumerate([1, 0, -1, 0, 1]):
        assert cos[i] == pytest.approx(expected)


def test_proper_sin():
    cos, sin = make_harmonic_features(np.array([0, 0.25, 0.5, 0.75, 1]), 1)
    for i, expected in enumerate([0, 1, 0, -1, 0]):
        assert sin[i] == pytest.approx(expected)


def test_outer_closer_than_through():
    cos, sin = make_harmonic_features(np.array([0, 2, 6], dtype=np.float), 7)
    outer_distance = np.sqrt(np.power(cos[0] - cos[2], 2) + np.power(sin[0] - sin[2], 2))
    through_distance = np.sqrt(np.power(cos[0] - cos[1], 2) + np.power(sin[0] - sin[1], 2))
    assert outer_distance < through_distance


def test_similar_distances():
    cos, sin = make_harmonic_features(np.array([0, 2, 4], dtype=np.float), 7)
    distance1 = np.sqrt(np.power(cos[0] - cos[1], 2) + np.power(sin[0] - sin[1], 2))
    distance2 = np.sqrt(np.power(cos[1] - cos[2], 2) + np.power(sin[1] - sin[2], 2))
    assert distance1 == distance2

