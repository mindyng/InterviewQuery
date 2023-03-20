import pandas as pd
import numpy as np


def make_harmonic_features(value: np.array, period: int) -> (np.array, np.array):
    value *= 2 * np.pi / period
    return np.cos(value), np.sin(value)


def extract_numerical_features(data: pd.DataFrame) -> pd.DataFrame:
    return data.reindex(columns=[
        'total_items',
        'subtotal',
        'num_distinct_items',
        'min_item_price',
        'max_item_price',
        'total_onshift_dashers',
        'total_busy_dashers',
        'total_outstanding_orders',
        'estimated_order_place_duration',
        'estimated_store_to_consumer_driving_duration'
    ])
