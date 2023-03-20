import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from app.features_extractors.categorical import one_hot_encode_column


def test_proper_columns_from_categories():
    df = pd.DataFrame({'col1': ['A', 'B', 'B']})
    encoder = OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(df.col1))
    features = one_hot_encode_column(df.col1, encoder)
    assert (features.columns == ['col1_A', 'col1_B']).all()


def test_proper_index_from_series():
    df = pd.DataFrame({'col1': ['A', 'B', 'B']}, index=[7, 8, 9])
    encoder = OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(df.col1))
    features = one_hot_encode_column(df.col1, encoder)
    assert (features.index == [7, 8, 9]).all()


def test_non_existing_category():
    df = pd.DataFrame({'col1': ['A', 'B', 'B']})
    encoder = OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(df.col1))
    df.loc[10, 'col1'] = 'C'
    features = one_hot_encode_column(df.col1, encoder)
    assert (features.loc[10, :] == 0).all()


def test_drop_nan_category_row():
    df = pd.DataFrame({'col1': ['A', 'B', 'B']})
    encoder = OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(df.col1))
    df.loc[10, 'col1'] = np.NaN
    features = one_hot_encode_column(df.col1, encoder)
    assert 10 not in features.index
