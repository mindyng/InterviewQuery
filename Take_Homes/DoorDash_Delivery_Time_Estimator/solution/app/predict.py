import argparse
import json
import os
import pickle
from typing import Dict

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from app.features_extractors.calendar import extract_calendar_features
from app.features_extractors.categorical import extract_categorical_features
from app.features_extractors.numerical import extract_numerical_features
from app.features_extractors.time import extract_time_features


def load_pseudo_json_data(path: str) -> pd.DataFrame:
    numeric_columns = [
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
    ]
    with open(path, 'rb') as file:
        file_rows = file.readlines()
    input_data = pd.DataFrame([json.loads(row) for row in file_rows])\
        .drop_duplicates('delivery_id')\
        .set_index('delivery_id')
    input_data['created_at'] = pd.to_datetime(input_data.created_at)
    for column_name in numeric_columns:
        numeric_column = pd.to_numeric(input_data[column_name], errors='coerce')
        input_data[column_name] = numeric_column.fillna(numeric_column.mean())
    return input_data


def extract_features(data: pd.DataFrame, encoders: Dict[str, OneHotEncoder]) -> pd.DataFrame:
    numerical_features = extract_numerical_features(data)
    categorical_features = extract_categorical_features(data, encoders)
    calendar_features = extract_calendar_features(data)
    time_features = extract_time_features(data)
    return pd.concat([
        numerical_features,
        categorical_features,
        calendar_features,
        time_features,
    ], axis=1)


def main(args):
    input_data = load_pseudo_json_data(args.input_path)
    model_persistence_structure = pickle.load(open(args.model_path, "rb"))
    features = extract_features(input_data, model_persistence_structure['encoders'])
    output_data = model_persistence_structure['model'].predict(features)
    pd.DataFrame(output_data, index=input_data.index, columns=['predicted_duration'])\
        .to_csv(args.output_path, sep='\t')


def file_path(path):
    if os.path.isfile(path):
        return os.path.abspath(path)
    else:
        raise argparse.ArgumentTypeError(f'File not found: {path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deliveries duration prediction.')
    parser.add_argument('input_path', metavar='INPUT_DATA', type=file_path,
                        help='path to JSON list of deliveries that​ you must predict​ on')
    parser.add_argument('model_path', metavar='TRAINED_MODEL', type=file_path,
                        help='path to pickled trained model ({model: <model>, encoders: <categories_encoders>}})')
    parser.add_argument('--output', dest='output_path', type=os.path.abspath, default='./output.tsv',
                        help='path to output TSV file')
    args = parser.parse_args()

    main(args)
    print('Finished prediction. Output saved into: ', args.output_path)
