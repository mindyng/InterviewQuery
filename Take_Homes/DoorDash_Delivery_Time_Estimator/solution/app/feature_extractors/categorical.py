from typing import Dict

import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def generate_encoders(data: pd.DataFrame) -> Dict[str, OneHotEncoder]:
    return {
        'store_primary_category':
            OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(data.store_primary_category).dropna()),
        'market_id':
            OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(data.market_id).dropna()),
        'order_protocol':
            OneHotEncoder(handle_unknown='ignore').fit(pd.DataFrame(data.order_protocol).dropna()),
    }


def one_hot_encode_column(values: pd.Series, encoder: OneHotEncoder) -> pd.DataFrame:
    values_without_nans = values.dropna()
    return pd.DataFrame(
        encoder.transform(pd.DataFrame(values_without_nans)).toarray(),
        index=values_without_nans.index,
        columns=encoder.categories_[0]
    ).add_prefix(values.name + '_')


def extract_categorical_features(data: pd.DataFrame, encoders: Dict[str, OneHotEncoder]) -> pd.DataFrame:
    return pd.concat([
        one_hot_encode_column(data.store_primary_category, encoders['store_primary_category']),
        one_hot_encode_column(data.market_id, encoders['market_id']),
        one_hot_encode_column(data.order_protocol, encoders['order_protocol']),
    ], axis=1).fillna(0)
